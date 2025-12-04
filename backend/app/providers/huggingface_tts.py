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
        """Generate speech audio using HuggingFace Space"""
        
        if not text:
            logger.warning("Empty text provided to TTS")
            return f"/static/audio/mock_audio_empty.wav"
        
        # Use HF Space API
        space_url = "https://abeachmad-macca-tts.hf.space/api/predict"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {"data": [text]}
                response = await client.post(space_url, json=payload)
                
                if response.status_code != 200:
                    error_msg = f"HF Space TTS returned status {response.status_code}: {response.text[:200]}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                result = response.json()
                # HF Space returns audio file URL
                audio_url_from_space = result.get("data", [None])[0]
                
                if not audio_url_from_space:
                    logger.warning("HF Space TTS returned no audio")
                    return f"/static/audio/mock_audio_{abs(hash(text)) % 1000}.wav"
                
                # Download audio from Space and save locally
                audio_response = await client.get(audio_url_from_space)
                audio_bytes = audio_response.content
                
                audio_url = self.storage_service.save_audio(audio_bytes, "wav")
                logger.info(f"TTS synthesis successful: {audio_url}")
                return audio_url
        except Exception as e:
            logger.error(f"HF Space TTS error: {e}")
            raise