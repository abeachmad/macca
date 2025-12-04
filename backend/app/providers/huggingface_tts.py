import logging
from gtts import gTTS
import tempfile
import os
from typing import Optional
from app.services.storage import StorageService

logger = logging.getLogger(__name__)

class HuggingFaceTTSProvider:
    def __init__(self, storage_service: StorageService):
        self.storage_service = storage_service
        logger.info(f"Initialized Google TTS Provider")
    
    async def synthesize_speech(self, text: str, voice: Optional[str] = None) -> str:
        """Generate speech using Google TTS (free)"""
        
        if not text:
            logger.warning("Empty text provided to TTS")
            return None
        
        if len(text) > 500:
            text = text[:500]
        
        temp_file = None
        try:
            logger.info(f"Synthesizing speech: {text[:50]}...")
            
            # Create temp file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                temp_file = f.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Read and save to storage
            with open(temp_file, 'rb') as f:
                audio_bytes = f.read()
            
            local_url = self.storage_service.save_audio(audio_bytes, "mp3")
            logger.info(f"TTS success: {local_url}")
            return local_url
                
        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            return None
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass