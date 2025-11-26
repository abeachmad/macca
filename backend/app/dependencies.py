from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional
import logging
from app.db.database import get_db
from app.db.models import User
from app.providers.mock import MockLLMProvider, MockASRProvider, MockTTSProvider
from app.providers.huggingface_llm import HuggingFaceLLMProvider
from app.providers.huggingface_asr import HuggingFaceASRProvider
from app.providers.huggingface_tts import HuggingFaceTTSProvider
from app.services.storage import StorageService
from app.config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

# Log AI provider mode at startup
if settings.use_mock_ai or not settings.hf_api_key:
    logger.info("🤖 AI Provider Mode: MOCK (USE_MOCK_AI=true or HF_API_KEY not set)")
else:
    logger.info(f"🤖 AI Provider Mode: HUGGING FACE (Model: {settings.hf_llm_model_id})")

# Provider factories
def get_llm_provider():
    if settings.use_mock_ai or not settings.hf_api_key:
        return MockLLMProvider()
    return HuggingFaceLLMProvider()

def get_asr_provider():
    if settings.use_mock_ai or not settings.hf_api_key:
        return MockASRProvider()
    return HuggingFaceASRProvider()

def get_tts_provider():
    if settings.use_mock_ai or not settings.hf_api_key:
        return MockTTSProvider()
    return HuggingFaceTTSProvider(get_storage_service())

def get_storage_service():
    return StorageService()

# Optional auth - returns User or None (for backward compatibility)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        return None

# Required auth - raises 401 if no valid token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Mock user for backward compatibility when no auth provided
mock_user_profile = {
    "id": "user_123",
    "name": "Demo User",
    "level": "B1",
    "goal": "job_interview",
    "explanation_language": "id",
    "common_issues": []
}