from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost/macca"
    
    # Hugging Face (ASR/TTS)
    hf_api_key: Optional[str] = None
    hf_api_base_url: str = "https://api-inference.huggingface.co"
    hf_asr_model_id: str = "openai/whisper-small"
    hf_tts_model_id: str = "facebook/mms-tts-eng"
    
    # Groq (LLM)
    groq_api_key: Optional[str] = None
    groq_model_id: str = "llama-3.1-8b-instant"
    
    # ElevenLabs (TTS)
    elevenlabs_api_key: Optional[str] = None
    
    # Feature flags
    use_mock_ai: bool = False
    
    # Logging
    log_level: str = "INFO"
    
    # CORS
    cors_origins: str = "*"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"

settings = Settings()