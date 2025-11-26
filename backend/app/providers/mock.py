import asyncio
from app.schemas.macca import (
    MaccaJsonResponse, MaccaFeedback, GrammarFeedback, 
    VocabularyFeedback, PronunciationFeedback, Drill,
    UserProfile, SessionContext
)

class MockLLMProvider:
    async def generate_macca_response(
        self, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        await asyncio.sleep(1)  # Simulate processing
        
        if session_context.mode == "live_conversation":
            return MaccaJsonResponse(
                reply=f"That's interesting! You mentioned '{user_text[:30]}...'. Can you tell me more about that?",
                feedback=MaccaFeedback(
                    better_sentence="I went to the office yesterday." if "go" in user_text.lower() else None,
                    grammar=[
                        GrammarFeedback(
                            issue="past_tense",
                            original_text=user_text,
                            explanation_language=user_profile.explanation_language,
                            explanation="Gunakan past tense untuk kejadian kemarin" if user_profile.explanation_language == "id" else "Use past tense for yesterday's events",
                            examples=["I went to work", "She visited her friend"]
                        )
                    ] if "go" in user_text.lower() else []
                ),
                drills=[
                    Drill(
                        type="repeat_sentence",
                        instruction="Please repeat this sentence:",
                        sentence="I went to the office yesterday."
                    )
                ] if "go" in user_text.lower() else [],
                next_prompt="Can you tell me more about your day?"
            )
        
        elif session_context.mode == "guided_lesson":
            return MaccaJsonResponse(
                reply="Great answer! Now let's move to the next part of our lesson.",
                feedback=MaccaFeedback(),
                drills=[],
                next_prompt="Tell me about your work experience."
            )
        
        else:  # pronunciation_coach
            return MaccaJsonResponse(
                reply="Good attempt! Let's practice that sound again.",
                feedback=MaccaFeedback(
                    pronunciation=[
                        PronunciationFeedback(
                            word=user_text.split()[0] if user_text.split() else "word",
                            target_sound="/θ/",
                            issue="th_sound",
                            tip="Put your tongue between your teeth",
                            severity="medium"
                        )
                    ]
                ),
                drills=[],
                next_prompt="Try saying 'think' again."
            )

class MockASRProvider:
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "en") -> str:
        await asyncio.sleep(0.5)
        return "I have five years of experience in software development."

class MockTTSProvider:
    async def synthesize_speech(self, text: str, language: str = "en") -> str:
        await asyncio.sleep(1)
        return f"/static/audio/mock_audio_{hash(text) % 1000}.wav"