import httpx
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class HuggingFaceASRProvider:
    def __init__(self):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_asr_model_id
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        logger.info(f"Initialized HF ASR Provider with model: {self.model_id}")
    
    async def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "en") -> str:
        """Transcribe audio using HuggingFace ASR"""
        
        if not audio_bytes:
            logger.warning("Empty audio bytes provided to ASR")
            return "Unable to transcribe audio"
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
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