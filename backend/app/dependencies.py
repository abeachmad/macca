from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.providers.mock import MockLLMProvider, MockASRProvider, MockTTSProvider
from app.providers.huggingface_llm import HuggingFaceLLMProvider
from app.providers.huggingface_asr import HuggingFaceASRProvider
from app.providers.huggingface_tts import HuggingFaceTTSProvider
from app.services.storage import StorageService
from app.config import settings

# Provider factories
def get_llm_provider():
    if settings.use_mock_ai:
        return MockLLMProvider()
    return HuggingFaceLLMProvider()

def get_asr_provider():
    if settings.use_mock_ai:
        return MockASRProvider()
    return HuggingFaceASRProvider()

def get_tts_provider():
    if settings.use_mock_ai:
        return MockTTSProvider()
    return HuggingFaceTTSProvider(get_storage_service())

def get_storage_service():
    return StorageService()

# Database dependency
def get_current_user():
    # Mock user for now - will implement JWT auth later
    return {
        "id": "user_123",
        "name": "User",
        "level": "B1",
        "goal": "job_interview",
        "explanation_language": "id"
    }

# Mock user profile for compatibility
mock_user_profile = {
    "id": "user_123",
    "name": "User",
    "level": "B1",
    "goal": "job_interview",
    "explanation_language": "id"
}