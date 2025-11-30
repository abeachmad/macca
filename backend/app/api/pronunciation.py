from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session as DBSession
from app.schemas.macca import PronunciationAnalysis, PronunciationFeedbackLegacy
from app.dependencies import mock_user_profile, get_asr_provider, get_llm_provider, get_current_user_optional, get_storage_service
from app.providers.base import ASRProvider, LLMProvider
from app.services.storage import StorageService
from app.db.database import get_db
from app.db.models import User, FeedbackIssue
import asyncio
import logging

logger = logging.getLogger(__name__)

# Max audio file size: 10MB
MAX_AUDIO_SIZE = 10 * 1024 * 1024

router = APIRouter(prefix="/pronunciation", tags=["pronunciation"])

@router.post("/analyze", response_model=List[PronunciationFeedbackLegacy])
async def analyze_pronunciation(
    analysis: PronunciationAnalysis,
    llm_provider: LLMProvider = Depends(get_llm_provider)
):
    """Text-only pronunciation analysis - uses AI for feedback"""
    
    # Use LLM to generate pronunciation feedback
    from app.schemas.macca import UserProfile, SessionContext
    
    user_profile = UserProfile(
        id="demo",
        name="User",
        level="B1",
        goal="daily_conversation",
        explanation_language="en",
        common_issues=[]
    )
    
    session_context = SessionContext(
        session_id="pronunciation",
        mode="pronunciation_coach"
    )
    
    prompt = f"Analyze pronunciation of the word '{analysis.word}'. Provide feedback on common pronunciation issues for Indonesian learners."
    
    try:
        response = await llm_provider.generate_macca_response(prompt, user_profile, session_context)
        
        # Convert to legacy format
        feedback = []
        for pron in response.feedback.pronunciation:
            feedback.append(PronunciationFeedbackLegacy(
                word=pron.word,
                target_sound=pron.target_sound,
                status="needs_work" if pron.severity in ["medium", "high"] else "good",
                tip_id=pron.tip,
                tip_en=pron.tip,
                score=70 if pron.severity == "high" else 80 if pron.severity == "medium" else 90
            ))
        
        if not feedback:
            # Default feedback if LLM doesn't provide pronunciation feedback
            feedback.append(PronunciationFeedbackLegacy(
                word=analysis.word,
                target_sound="overall",
                status="good",
                tip_id="Practice this word more to improve clarity.",
                tip_en="Practice this word more to improve clarity.",
                score=85
            ))
        
        return feedback
    except Exception as e:
        logger.error(f"Error in pronunciation analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze pronunciation")

@router.post("/analyze/audio", response_model=List[PronunciationFeedbackLegacy])
async def analyze_pronunciation_audio(
    audio: UploadFile = File(...),
    word: str = Form(...),
    asr_provider: ASRProvider = Depends(get_asr_provider),
    storage_service: StorageService = Depends(get_storage_service),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    """Audio-based pronunciation analysis"""
    
    user_id = str(current_user.id) if current_user else "anonymous"
    logger.info(f"POST /pronunciation/analyze/audio - user_id={user_id}, word={word}")
    
    # Read and validate audio size
    audio_bytes = await audio.read()
    if len(audio_bytes) > MAX_AUDIO_SIZE:
        logger.warning(f"Audio file too large: {len(audio_bytes)} bytes (max {MAX_AUDIO_SIZE})")
        raise HTTPException(
            status_code=413,
            detail=f"Audio file too large (max {MAX_AUDIO_SIZE // (1024*1024)} MB)"
        )
    
    audio_url = storage_service.save_audio(audio_bytes, "wav")
    
    # Transcribe audio
    transcript = await asr_provider.transcribe_audio(audio_bytes)
    
    # Simple pronunciation analysis based on transcript
    # In production, this would use more sophisticated analysis
    feedback = []
    
    # Check if transcribed word matches target word
    if transcript.lower().strip() == word.lower().strip():
        feedback.append(PronunciationFeedbackLegacy(
            word=word,
            target_sound="overall",
            status="excellent",
            tip_id="Sempurna! Pengucapan Anda sangat jelas.",
            tip_en="Perfect! Your pronunciation is very clear.",
            score=95
        ))
    else:
        feedback.append(PronunciationFeedbackLegacy(
            word=word,
            target_sound="overall",
            status="needs_work",
            tip_id=f"Coba lagi. Saya mendengar '{transcript}' bukan '{word}'.",
            tip_en=f"Try again. I heard '{transcript}' not '{word}'.",
            score=50
        ))
    
    # Persist feedback if user is authenticated
    if current_user:
        issue = FeedbackIssue(
            user_id=current_user.id,
            session_id=None,
            utterance_id=None,
            type="pronunciation",
            issue_code=word,
            detail={"word": word, "transcript": transcript, "audio_url": audio_url}
        )
        db.add(issue)
        db.commit()
    
    return feedback