import httpx
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class HuggingFaceASRProvider:
    def __init__(self):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_asr_model_id
        self.base_url = settings.hf_api_base_url
        logger.info(f"Initialized HF ASR Provider with model: {self.model_id}, base: {self.base_url}")
    
    async def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "en") -> str:
        """Transcribe audio using HuggingFace ASR"""
        
        # Early exit if no API key
        if not self.api_key:
            logger.warning("HF ASR provider called without API key, returning fallback")
            return "Unable to transcribe audio"
        
        if not audio_bytes:
            logger.warning("Empty audio bytes provided to ASR")
            return "Unable to transcribe audio"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model_id}",
                    content=audio_bytes,
                    headers=headers
                )
                
                if response.status_code != 200:
                    logger.warning(f"HF ASR API returned status {response.status_code}: {response.text[:200]}")
                    return "Unable to transcribe audio"
                
                result = response.json()
                transcript = result.get("text", "Unable to transcribe audio")
                logger.info(f"ASR transcription successful: {transcript[:50]}...")
                return transcript
        except (httpx.TimeoutException, httpx.RequestError) as e:
            logger.error(f"HF ASR API request failed: {e}")
            return "Unable to transcribe audio"
        except Exception as e:
            logger.error(f"Unexpected error in HF ASR provider: {e}")
            return "Unable to transcribe audio"