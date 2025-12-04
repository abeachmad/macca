import logging
import httpx
import tempfile
import os
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class HuggingFaceASRProvider:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
        logger.info(f"Initialized Groq ASR Provider with whisper-large-v3")
    
    async def transcribe_audio(self, audio_bytes: bytes, language: Optional[str] = "en") -> str:
        """Transcribe audio using Groq Whisper API"""
        
        if not audio_bytes:
            logger.warning("Empty audio bytes provided to ASR")
            return "Unable to transcribe audio"
        
        temp_file = None
        try:
            logger.info(f"Transcribing audio ({len(audio_bytes)} bytes) with Groq Whisper")
            
            # Save to temp file (Groq needs multipart/form-data)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
                f.write(audio_bytes)
                temp_file = f.name
            
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                with open(temp_file, 'rb') as audio_file:
                    files = {"file": ("audio.webm", audio_file, "audio/webm")}
                    data = {"model": "whisper-large-v3"}
                    
                    response = await client.post(
                        self.api_url,
                        headers=headers,
                        files=files,
                        data=data
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    transcript = result.get("text", "")
                    logger.info(f"ASR transcription: {transcript[:100]}")
                    return transcript
                else:
                    logger.warning(f"Groq ASR API returned {response.status_code}: {response.text[:200]}")
                    return "[Audio transcription unavailable]"
            
        except Exception as e:
            logger.error(f"Groq ASR error: {e}")
            return "[Audio transcription unavailable]"
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass