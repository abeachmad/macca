#!/usr/bin/env python3
"""Unit tests for LLM JSON parsing"""

import sys
import os
# Set test environment before importing
os.environ["USE_MOCK_AI"] = "true"
os.environ["HF_API_KEY"] = ""
sys.path.insert(0, os.path.dirname(__file__))

from app.providers.huggingface_llm import HuggingFaceLLMProvider
from app.schemas.macca import UserProfile, SessionContext

def test_json_extraction():
    """Test that JSON can be extracted from various response formats"""
    provider = HuggingFaceLLMProvider()
    
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
    
    # Test 1: Valid JSON in response
    valid_json = '''
    {
        "reply": "Great job!",
        "feedback": {
            "better_sentence": null,
            "grammar": [],
            "vocabulary": [],
            "pronunciation": []
        },
        "drills": [],
        "next_prompt": "What else?"
    }
    '''
    result = provider._parse_llm_response(valid_json, "test", user_profile, session_context)
    assert result.reply == "Great job!"
    print("✅ Test 1: Valid JSON extraction passed")
    
    # Test 2: JSON with extra text before/after
    json_with_extra = '''
    Here is my response:
    {
        "reply": "Good work!",
        "feedback": {"better_sentence": null, "grammar": [], "vocabulary": [], "pronunciation": []},
        "drills": [],
        "next_prompt": "Continue?"
    }
    That's all!
    '''
    result = provider._parse_llm_response(json_with_extra, "test", user_profile, session_context)
    assert result.reply == "Good work!"
    print("✅ Test 2: JSON with extra text extraction passed")
    
    # Test 3: Invalid JSON - should fallback
    invalid_json = "This is not JSON at all"
    result = provider._parse_llm_response(invalid_json, "I go yesterday", user_profile, session_context)
    assert result.reply  # Should have some reply
    assert "yesterday" in result.reply or result.feedback.grammar  # Should detect grammar issue
    print("✅ Test 3: Invalid JSON fallback passed")
    
    # Test 4: Malformed JSON - should fallback
    malformed_json = '{"reply": "Test", "feedback": {'
    result = provider._parse_llm_response(malformed_json, "test", user_profile, session_context)
    assert result.reply  # Should have fallback reply
    print("✅ Test 4: Malformed JSON fallback passed")
    
    print("\n🎉 All JSON parsing tests passed!")

if __name__ == "__main__":
    test_json_extraction()
