from fastapi import APIRouter
from typing import List
from app.schemas.macca import PronunciationAnalysis, PronunciationFeedbackLegacy
from app.dependencies import mock_user_profile
import asyncio

router = APIRouter(prefix="/pronunciation", tags=["pronunciation"])

@router.post("/analyze", response_model=List[PronunciationFeedbackLegacy])
async def analyze_pronunciation(analysis: PronunciationAnalysis):
    await asyncio.sleep(1.5)  # Simulate processing
    
    return [
        PronunciationFeedbackLegacy(
            word=analysis.word,
            target_sound="/θ/",
            status="needs_work",
            tip_id="Letakkan lidah di antara gigi dan tiup udara perlahan: 'th-ink'.",
            tip_en="Put your tongue between your teeth and blow air softly: 'th-ink'.",
            score=65
        ),
        PronunciationFeedbackLegacy(
            word=analysis.word,
            target_sound="vowel /ɪ/",
            status="good",
            tip_id="Vokal pendek sudah bagus!",
            tip_en="Short vowel is good!",
            score=82
        )
    ]