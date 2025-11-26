from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.macca import (
    ConversationTurn, ConversationResponse, 
    UserProfile, SessionContext, MaccaFeedback, Drill
)
from app.providers.base import LLMProvider, TTSProvider
from app.dependencies import get_llm_provider, get_tts_provider, get_current_user

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
    current_user: dict = Depends(get_current_user)
):
    session_id = f"sess_{hash(str(request.dict())) % 10000}"
    
    initial_prompts = {
        "live_conversation": f"Hi {current_user['name']}! Let's have a natural conversation. How was your day?",
        "guided_lesson": f"Welcome to today's lesson, {current_user['name']}! Let's start with introducing yourself.",
        "pronunciation_coach": f"Hi {current_user['name']}! Let's practice pronunciation. Say the word 'think'."
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
    current_user: dict = Depends(get_current_user)
):
    user_profile = UserProfile(**current_user, common_issues=[])
    session_context = SessionContext(
        session_id="mock_session",
        mode="live_conversation" if turn.mode == "live" else 
              "guided_lesson" if turn.mode == "guided" else 
              "pronunciation_coach"
    )
    
    macca_response = await llm_provider.generate_macca_response(
        turn.user_text, user_profile, session_context
    )
    
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