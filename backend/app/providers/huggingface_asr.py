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
        """Transcribe audio using HuggingFace Space"""
        
        if not audio_bytes:
            logger.warning("Empty audio bytes provided to ASR")
            return "Unable to transcribe audio"
        
        # Use HF Space API
        space_url = "https://abeachmad-macca-asr.hf.space/api/predict"
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                files = {"data": ("audio.wav", audio_bytes, "audio/wav")}
                response = await client.post(space_url, files=files)
                
                if response.status_code != 200:
                    error_msg = f"HF Space ASR returned status {response.status_code}: {response.text[:200]}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                result = response.json()
                transcript = result.get("data", ["Unable to transcribe"])[0]
                logger.info(f"ASR transcription successful: {transcript[:50]}...")
                return transcript
        except Exception as e:
            logger.error(f"HF Space ASR error: {e}")
            raise