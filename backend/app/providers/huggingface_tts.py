import logging
from typing import Optional
from app.services.storage import StorageService

logger = logging.getLogger(__name__)

class HuggingFaceTTSProvider:
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service
        logger.info(f"TTS Provider initialized (disabled in production)")
    
    async def synthesize_speech(self, text: str, voice: Optional[str] = None) -> str:
        """TTS disabled in production to prevent serverless crashes"""
        logger.info(f"TTS disabled: {text[:50]}...")
        return None