import httpx
import logging
from typing import Optional
from app.config import settings
from app.services.storage import StorageService

logger = logging.getLogger(__name__)

class HuggingFaceTTSProvider:
    def __init__(self, storage_service: StorageService):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_tts_model_id
        self.base_url = settings.hf_api_base_url
        self.storage_service = storage_service
        logger.info(f"Initialized HF TTS Provider with model: {self.model_id}, base: {self.base_url}")
    
    async def synthesize_speech(self, text: str, voice: Optional[str] = None) -> str:
        """Generate speech audio using HuggingFace TTS"""
        
        # Early exit if no API key
        if not self.api_key:
            logger.warning("HF TTS provider called without API key, returning fallback")
            return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"
        
        if not text:
            logger.warning("Empty text provided to TTS")
            return f"/static/audio/mock_audio_empty.wav"
        
        payload = {"inputs": text}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model_id}",
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    logger.warning(f"HF TTS API returned status {response.status_code}: {response.text[:200]}")
                    return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"
                
                # Save audio bytes and return URL
                audio_bytes = response.content
                if not audio_bytes:
                    logger.warning("HF TTS returned empty audio")
                    return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"
                
                audio_url = self.storage_service.save_audio(audio_bytes, "wav")
                logger.info(f"TTS synthesis successful: {audio_url}")
                return audio_url
        except (httpx.TimeoutException, httpx.RequestError) as e:
            logger.error(f"HF TTS API request failed: {e}")
            return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"
        except Exception as e:
            logger.error(f"Unexpected error in HF TTS provider: {e}")
            return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"