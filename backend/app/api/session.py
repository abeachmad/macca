from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

# Max audio file size: 10MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024
from app.schemas.macca import (
    ConversationTurn, ConversationResponse, 
    UserProfile, SessionContext, MaccaFeedback, Drill
)
from app.providers.base import LLMProvider, TTSProvider, ASRProvider
from app.dependencies import get_llm_provider, get_tts_provider, get_asr_provider, get_current_user_optional, get_storage_service
from app.db.database import get_db
from app.db.models import User, Session, Utterance, FeedbackIssue
from app.services.storage import StorageService

router = APIRouter(prefix="/session", tags=["session"])

class SessionStartRequest(BaseModel):
    mode: str
    topic: Optional[str] = None
    lesson_id: Optional[str] = None

class SessionStartResponse(BaseModel):
    session_id: str
    initial_prompt: str
    lesson_step: Optional[int] = None
    lesson_title: Optional[str] = None
    total_steps: Optional[int] = None

@router.post("/start", response_model=SessionStartResponse)
async def start_session(
    request: SessionStartRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    # Create session in DB if user is authenticated
    if current_user:
        session = Session(
            user_id=current_user.id,
            mode=request.mode,
            topic=request.topic,
            lesson_id=request.lesson_id
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = str(session.id)
        user_name = current_user.name
    else:
        # Mock session for backward compatibility
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        user_name = "there"
    
    initial_prompts = {
        "live_conversation": f"Hi {user_name}! Let's have a natural conversation. How was your day?",
        "guided_lesson": f"Welcome to today's lesson, {user_name}! Let's start with introducing yourself.",
        "pronunciation_coach": f"Hi {user_name}! Let's practice pronunciation. Say the word 'think'."
    }
    
    return SessionStartResponse(
        session_id=session_id,
        initial_prompt=initial_prompts.get(request.mode, "Let's start practicing!"),
        lesson_step=1 if request.mode == "guided_lesson" else None,
        lesson_title="Job Interview Practice" if request.lesson_id else None,
        total_steps=4 if request.mode == "guided_lesson" else None
    )

@router.post("/turn", response_model=ConversationResponse)
async def process_conversation_turn(
    turn: ConversationTurn,
    llm_provider: LLMProvider = Depends(get_llm_provider),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    # Build user profile
    if current_user:
        user_profile = UserProfile(
            id=str(current_user.id),
            name=current_user.name,
            level=current_user.level,
            goal=current_user.goal,
            explanation_language=current_user.explanation_language,
            common_issues=[]
        )
    else:
        from app.dependencies import mock_user_profile
        user_profile = UserProfile(**mock_user_profile)
    
    session_context = SessionContext(
        session_id="mock_session",
        mode="live_conversation" if turn.mode == "live" else 
              "guided_lesson" if turn.mode == "guided" else 
              "pronunciation_coach"
    )
    
    # Use provided text (audio support can be added via separate endpoint if needed)
    transcript = turn.user_text
    
    # Generate response from LLM
    macca_response = await llm_provider.generate_macca_response(
        transcript, user_profile, session_context
    )
    
    # Persist to DB if user is authenticated
    if current_user:
        # Find or create session (simplified - in production, track session_id properly)
        session = db.query(Session).filter(
            Session.user_id == current_user.id
        ).order_by(Session.started_at.desc()).first()
        
        if session:
            # Save user utterance
            user_utterance = Utterance(
                session_id=session.id,
                user_id=current_user.id,
                role="user",
                transcript=turn.user_text
            )
            db.add(user_utterance)
            
            # Save assistant utterance
            assistant_utterance = Utterance(
                session_id=session.id,
                user_id=current_user.id,
                role="assistant",
                transcript=macca_response.reply,
                raw_llm_json=macca_response.dict()
            )
            db.add(assistant_utterance)
            db.commit()
            db.refresh(assistant_utterance)
            
            db.commit()
    
    # Convert to legacy format for frontend compatibility
    feedback = {}
    if macca_response.grammar_feedback:
        feedback["grammar_ok"] = False
        feedback["tip_id"] = macca_response.grammar_feedback[0].get("explanation", "Check grammar")
    else:
        feedback["grammar_ok"] = True
        feedback["fluency_score"] = 85
        feedback["tip_id"] = "Good! Try using more adjectives."
    
    if turn.mode == "guided":
        feedback["step_complete"] = True
        feedback["encouragement_id"] = "Perfect! Let's continue."
    
    return ConversationResponse(
        macca_text=macca_response.reply,
        feedback=feedback,
        next_step="step_3" if turn.mode == "guided" else None
    )

@router.post("/turn/audio", response_model=ConversationResponse)
async def process_conversation_turn_audio(
    audio: UploadFile = File(...),
    mode: str = Form("live"),
    session_id: Optional[str] = Form(None),
    llm_provider: LLMProvider = Depends(get_llm_provider),
    asr_provider: ASRProvider = Depends(get_asr_provider),
    tts_provider: TTSProvider = Depends(get_tts_provider),
    storage_service: StorageService = Depends(get_storage_service),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    """Process conversation turn with audio input"""
    
    user_id = str(current_user.id) if current_user else "anonymous"
    logger.info(f"POST /session/turn/audio - user_id={user_id}, session_id={session_id}, mode={mode}")
    
    # Read and validate audio size
    audio_bytes = await audio.read()
    if len(audio_bytes) > MAX_AUDIO_SIZE:
        logger.warning(f"Audio file too large: {len(audio_bytes)} bytes (max {MAX_AUDIO_SIZE})")
        raise HTTPException(
            status_code=413,
            detail=f"Audio file too large (max {MAX_AUDIO_SIZE // (1024*1024)} MB)"
        )
    
    # Build user profile
    if current_user:
        user_profile = UserProfile(
            id=str(current_user.id),
            name=current_user.name,
            level=current_user.level,
            goal=current_user.goal,
            explanation_language=current_user.explanation_language,
            common_issues=[]
        )
    else:
        from app.dependencies import mock_user_profile
        user_profile = UserProfile(**mock_user_profile)
    
    session_context = SessionContext(
        session_id=session_id or "mock_session",
        mode="live_conversation" if mode == "live" else 
              "guided_lesson" if mode == "guided" else 
              "pronunciation_coach"
    )
    
    user_audio_url = storage_service.save_audio(audio_bytes, "wav")
    
    # Transcribe audio
    transcript = await asr_provider.transcribe_audio(audio_bytes)
    
    # Generate response from LLM
    macca_response = await llm_provider.generate_macca_response(
        transcript, user_profile, session_context
    )
    
    # Generate TTS for response
    macca_audio_url = await tts_provider.synthesize_speech(macca_response.reply)
    
    # Persist to DB if user is authenticated
    if current_user:
        session = db.query(Session).filter(
            Session.user_id == current_user.id
        ).order_by(Session.started_at.desc()).first()
        
        if session:
            # Save user utterance with audio
            user_utterance = Utterance(
                session_id=session.id,
                user_id=current_user.id,
                role="user",
                transcript=transcript,
                audio_url=user_audio_url
            )
            db.add(user_utterance)
            
            # Save assistant utterance with audio
            assistant_utterance = Utterance(
                session_id=session.id,
                user_id=current_user.id,
                role="assistant",
                transcript=macca_response.reply,
                audio_url=macca_audio_url,
                raw_llm_json=macca_response.dict()
            )
            db.add(assistant_utterance)
            db.commit()
            db.refresh(assistant_utterance)
            
            db.commit()
    
    # Convert to legacy format for frontend compatibility
    feedback = {}
    if macca_response.grammar_feedback:
        feedback["grammar_ok"] = False
        feedback["tip_id"] = macca_response.grammar_feedback[0].get("explanation", "Check grammar")
    else:
        feedback["grammar_ok"] = True
        feedback["fluency_score"] = 85
        feedback["tip_id"] = "Good! Try using more adjectives."
    
    if mode == "guided":
        feedback["step_complete"] = True
        feedback["encouragement_id"] = "Perfect! Let's continue."
    
    return ConversationResponse(
        macca_text=macca_response.reply,
        macca_audio_url=macca_audio_url,
        feedback=feedback,
        next_step="step_3" if mode == "guided" else None
    )