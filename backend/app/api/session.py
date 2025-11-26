from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from datetime import datetime
import uuid
from app.schemas.macca import (
    ConversationTurn, ConversationResponse, 
    UserProfile, SessionContext, MaccaFeedback, Drill
)
from app.providers.base import LLMProvider, TTSProvider
from app.dependencies import get_llm_provider, get_tts_provider, get_current_user_optional
from app.db.database import get_db
from app.db.models import User, Session, Utterance, FeedbackIssue

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
    
    # Generate response from LLM
    macca_response = await llm_provider.generate_macca_response(
        turn.user_text, user_profile, session_context
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
            
            # Save feedback issues
            for grammar in macca_response.feedback.grammar:
                issue = FeedbackIssue(
                    user_id=current_user.id,
                    session_id=session.id,
                    utterance_id=assistant_utterance.id,
                    type="grammar",
                    issue_code=grammar.issue,
                    detail=grammar.dict()
                )
                db.add(issue)
            
            for vocab in macca_response.feedback.vocabulary:
                issue = FeedbackIssue(
                    user_id=current_user.id,
                    session_id=session.id,
                    utterance_id=assistant_utterance.id,
                    type="vocabulary",
                    issue_code=vocab.word,
                    detail=vocab.dict()
                )
                db.add(issue)
            
            for pron in macca_response.feedback.pronunciation:
                issue = FeedbackIssue(
                    user_id=current_user.id,
                    session_id=session.id,
                    utterance_id=assistant_utterance.id,
                    type="pronunciation",
                    issue_code=pron.word,
                    detail=pron.dict()
                )
                db.add(issue)
            
            db.commit()
    
    # Convert to legacy format for frontend compatibility
    feedback = {}
    if macca_response.feedback.grammar:
        feedback["grammar_ok"] = False
        feedback["tip_id"] = macca_response.feedback.grammar[0].explanation
    else:
        feedback["grammar_ok"] = True
        feedback["fluency_score"] = 85
        feedback["tip_id"] = ("Bagus! Coba gunakan lebih banyak kata sifat." 
                             if user_profile.explanation_language == "id" 
                             else "Good! Try using more adjectives.")
    
    if turn.mode == "guided":
        feedback["step_complete"] = True
        feedback["encouragement_id"] = ("Sempurna! Mari lanjutkan." 
                                       if user_profile.explanation_language == "id" 
                                       else "Perfect! Let's continue.")
    
    return ConversationResponse(
        macca_text=macca_response.reply,
        feedback=feedback,
        next_step="step_3" if turn.mode == "guided" else None
    )