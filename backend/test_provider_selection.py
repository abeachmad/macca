#!/usr/bin/env python3
"""Test provider selection logic"""

import os
# Set test environment before importing
os.environ["USE_MOCK_AI"] = "true"
os.environ["HF_API_KEY"] = ""
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.dependencies import get_llm_provider, get_asr_provider, get_tts_provider
from app.providers.mock import MockLLMProvider, MockASRProvider, MockTTSProvider
from app.providers.huggingface_llm import HuggingFaceLLMProvider
from app.providers.huggingface_asr import HuggingFaceASRProvider
from app.providers.huggingface_tts import HuggingFaceTTSProvider
from app.config import settings

def test_mock_providers_in_test_mode():
    """Verify that mock providers are used when USE_MOCK_AI=true"""
    
    print(f"Testing with USE_MOCK_AI={settings.use_mock_ai}, HF_API_KEY={'set' if settings.hf_api_key else 'not set'}")
    
    # Get providers
    llm = get_llm_provider()
    asr = get_asr_provider()
    tts = get_tts_provider()
    
    # Verify they are mock providers
    assert isinstance(llm, MockLLMProvider), f"Expected MockLLMProvider, got {type(llm)}"
    assert isinstance(asr, MockASRProvider), f"Expected MockASRProvider, got {type(asr)}"
    assert isinstance(tts, MockTTSProvider), f"Expected MockTTSProvider, got {type(tts)}"
    
    print("✅ Test 1: Mock providers are used in test mode")

def test_hf_providers_not_instantiated():
    """Verify HuggingFace providers are not instantiated in test mode"""
    
    # This test verifies that the dependency injection returns mock providers
    # and doesn't instantiate HF providers at all
    
    llm = get_llm_provider()
    asr = get_asr_provider()
    tts = get_tts_provider()
    
    # Verify none are HF providers
    assert not isinstance(llm, HuggingFaceLLMProvider), "HuggingFaceLLMProvider should not be used in test mode"
    assert not isinstance(asr, HuggingFaceASRProvider), "HuggingFaceASRProvider should not be used in test mode"
    assert not isinstance(tts, HuggingFaceTTSProvider), "HuggingFaceTTSProvider should not be used in test mode"
    
    print("✅ Test 2: HuggingFace providers are not instantiated in test mode")

def test_mock_provider_behavior():
    """Verify mock providers return expected responses without network calls"""
    import asyncio
    from app.schemas.macca import UserProfile, SessionContext
    
    llm = get_llm_provider()
    
    user_profile = UserProfile(
        id="test_user",
        name="Test",
        level="B1",
        goal="job_interview",
        explanation_language="en",
        common_issues=[]
    )
    
    session_context = SessionContext(
        session_id="test_session",
        mode="live_conversation"
    )
    
    # Call the mock provider
    response = asyncio.run(llm.generate_macca_response(
        "I go to office yesterday",
        user_profile,
        session_context
    ))
    
    # Verify we got a response
    assert response.reply, "Mock provider should return a reply"
    assert response.feedback, "Mock provider should return feedback"
    
    print("✅ Test 3: Mock providers work without network calls")

if __name__ == "__main__":
    test_mock_providers_in_test_mode()
    test_hf_providers_not_instantiated()
    test_mock_provider_behavior()
    print("\n🎉 All provider selection tests passed!")
