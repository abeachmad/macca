from typing import Protocol
from app.schemas.macca import MaccaJsonResponse, UserProfile, SessionContext

class ASRProvider(Protocol):
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "en") -> str:
        """Transcribe audio to text"""
        ...

class LLMProvider(Protocol):
    async def generate_macca_response(
        self, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        """Generate Macca's response with feedback"""
        ...

class TTSProvider(Protocol):
    async def synthesize_speech(self, text: str, language: str = "en") -> str:
        """Generate speech audio and return URL"""
        ...