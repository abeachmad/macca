from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost/macca"
    
    # Hugging Face
    hf_api_key: Optional[str] = None
    hf_llm_model_id: str = "SeaLLMs/SeaLLMs-v3-7B-Chat"
    hf_asr_model_id: str = "openai/whisper-large-v3-turbo"
    hf_tts_model_id: str = "audo/seamless-m4t-v2-large"
    
    # Feature flags
    use_mock_ai: bool = True
    
    # CORS
    cors_origins: str = "*"
    
    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"

settings = Settings()