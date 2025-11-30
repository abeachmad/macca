from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uuid

# Core types
ExplanationLanguage = Literal["id", "en"]
UserGoal = Literal["job_interview", "study", "daily_conversation"]
SessionMode = Literal["live_conversation", "guided_lesson", "pronunciation_coach"]
PronunciationSeverity = Literal["low", "medium", "high"]
DrillType = Literal["repeat_sentence", "short_answer"]

# Feedback schemas
class GrammarFeedback(BaseModel):
    issue: str
    original_text: str
    explanation_language: ExplanationLanguage
    explanation: str
    examples: List[str]

class VocabularyFeedback(BaseModel):
    word: str
    translation: str
    example: str

class PronunciationFeedback(BaseModel):
    word: str
    target_sound: str
    issue: str
    tip: str
    severity: PronunciationSeverity

class MaccaFeedback(BaseModel):
    better_sentence: Optional[str] = None
    grammar: List[GrammarFeedback] = []
    vocabulary: List[VocabularyFeedback] = []
    pronunciation: List[PronunciationFeedback] = []

class Drill(BaseModel):
    type: DrillType
    instruction: str
    sentence: Optional[str] = None
    question: Optional[str] = None

class MaccaJsonResponse(BaseModel):
    version: Optional[str] = "1.0"
    reply: str
    grammar_feedback: List[dict] = []
    vocabulary_feedback: List[dict] = []
    pronunciation_feedback: List[dict] = []

# User schemas
class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    level: str  # A1, A2, B1, B2, C1, C2
    goal: UserGoal
    explanation_language: ExplanationLanguage
    common_issues: List[str] = []

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    goal: Optional[UserGoal] = None
    explanation_language: Optional[ExplanationLanguage] = None

# Session schemas
class SessionContext(BaseModel):
    session_id: str
    mode: SessionMode
    topic: Optional[str] = None
    lesson_id: Optional[str] = None
    lesson_objective: Optional[str] = None
    target_grammar: List[str] = []
    target_vocabulary: List[str] = []
    lesson_step: Optional[int] = None
    short_summary: Optional[str] = None

class SessionStart(BaseModel):
    mode: SessionMode
    topic: Optional[str] = None
    lesson_id: Optional[str] = None

class SessionTurn(BaseModel):
    session_id: str
    user_text: str
    turn_number: Optional[int] = None

# Legacy compatibility schemas (matching current API)
class ConversationTurn(BaseModel):
    user_text: str
    mode: Literal["live", "guided", "pronunciation"]

class ConversationResponse(BaseModel):
    macca_text: str
    feedback: Optional[dict] = None
    next_step: Optional[str] = None

class PronunciationAnalysis(BaseModel):
    word: str
    audio_data: Optional[str] = None

class PronunciationFeedbackLegacy(BaseModel):
    word: str
    target_sound: str
    status: Literal["good", "needs_work", "excellent"]
    tip_id: str
    tip_en: str
    score: int

class Lesson(BaseModel):
    id: str
    title: str
    subtitle: str
    steps: List[str]
    current_step: int = 1