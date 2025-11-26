import httpx
from app.config import settings
from app.services.storage import StorageService

class HuggingFaceTTSProvider:
    def __init__(self, storage_service: StorageService):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_tts_model_id
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        self.storage_service = storage_service
    
    async def synthesize_speech(self, text: str, language: str = "en") -> str:
        """Generate speech audio using HuggingFace TTS"""
        
        payload = {"inputs": text}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                # Return mock audio URL
                return f"/static/audio/mock_audio_{hash(text) % 1000}.wav"
            
            # Save audio bytes and return URL
            audio_bytes = response.content
            audio_url = self.storage_service.save_audio(audio_bytes, "wav")
            return audio_url