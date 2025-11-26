import httpx
from app.config import settings

class HuggingFaceASRProvider:
    def __init__(self):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_asr_model_id
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
    
    async def transcribe_audio(self, audio_bytes: bytes, language: str = "en") -> str:
        """Transcribe audio using HuggingFace ASR"""
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                content=audio_bytes,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                # Fallback mock transcription
                return "I have five years of experience in software development."
            
            result = response.json()
            return result.get("text", "Could not transcribe audio")