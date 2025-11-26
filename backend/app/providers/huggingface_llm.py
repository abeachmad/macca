import httpx
import json
import re
from typing import Optional
from app.config import settings
from app.schemas.macca import (
    MaccaJsonResponse, MaccaFeedback, GrammarFeedback, 
    VocabularyFeedback, PronunciationFeedback, Drill,
    UserProfile, SessionContext
)

class HuggingFaceLLMProvider:
    def __init__(self):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_llm_model_id
        self.base_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
    
    async def generate_macca_response(
        self, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        """Generate Macca's response using HuggingFace LLM"""
        
        system_prompt = self._build_system_prompt(user_profile, session_context)
        user_prompt = f"User said: '{user_text}'\n\nProvide your response as valid JSON:"
        
        payload = {
            "inputs": f"{system_prompt}\n\n{user_prompt}",
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "return_full_text": False
            }
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url, 
                json=payload, 
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code != 200:
                # Fallback to mock response
                return self._fallback_response(user_text, user_profile, session_context)
            
            result = response.json()
            generated_text = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
            
            return self._parse_llm_response(generated_text, user_text, user_profile, session_context)
    
    def _build_system_prompt(self, user_profile: UserProfile, session_context: SessionContext) -> str:
        """Build system prompt for the LLM"""
        lang = "Indonesian" if user_profile.explanation_language == "id" else "English"
        
        prompt = f"""You are Macca, an AI English speaking coach for Indonesian learners.

User Profile:
- Name: {user_profile.name}
- Level: {user_profile.level}
- Goal: {user_profile.goal}
- Explanation Language: {lang}

Session Context:
- Mode: {session_context.mode}
- Topic: {session_context.topic or "General conversation"}

Instructions:
1. Provide natural, encouraging responses
2. Give constructive feedback on grammar, vocabulary, and pronunciation
3. Suggest improvements and provide examples
4. Always respond in valid JSON format matching this structure:

{{
  "reply": "Your encouraging response here",
  "feedback": {{
    "better_sentence": "Corrected sentence if needed",
    "grammar": [{{
      "issue": "grammar_issue_type",
      "original_text": "original text",
      "explanation_language": "{user_profile.explanation_language}",
      "explanation": "Grammar explanation in {lang}",
      "examples": ["example1", "example2"]
    }}],
    "vocabulary": [{{
      "word": "word",
      "translation": "translation",
      "example": "example sentence"
    }}],
    "pronunciation": [{{
      "word": "word",
      "target_sound": "/sound/",
      "issue": "issue_description",
      "tip": "pronunciation tip",
      "severity": "low|medium|high"
    }}]
  }},
  "drills": [{{
    "type": "repeat_sentence|short_answer",
    "instruction": "instruction text",
    "sentence": "sentence to repeat (optional)",
    "question": "question to answer (optional)"
  }}],
  "next_prompt": "Follow-up question or prompt"
}}"""
        
        return prompt
    
    def _parse_llm_response(
        self, 
        generated_text: str, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        """Parse LLM response and extract JSON"""
        
        # Try to extract JSON from the response
        json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                # Validate and create MaccaJsonResponse
                return MaccaJsonResponse(
                    reply=data.get("reply", "Great! Let's continue practicing."),
                    feedback=MaccaFeedback(
                        better_sentence=data.get("feedback", {}).get("better_sentence"),
                        grammar=[
                            GrammarFeedback(**g) for g in data.get("feedback", {}).get("grammar", [])
                        ],
                        vocabulary=[
                            VocabularyFeedback(**v) for v in data.get("feedback", {}).get("vocabulary", [])
                        ],
                        pronunciation=[
                            PronunciationFeedback(**p) for p in data.get("feedback", {}).get("pronunciation", [])
                        ]
                    ),
                    drills=[Drill(**d) for d in data.get("drills", [])],
                    next_prompt=data.get("next_prompt", "What would you like to talk about next?")
                )
            except (json.JSONDecodeError, KeyError, TypeError):
                pass
        
        # Fallback to mock response if parsing fails
        return self._fallback_response(user_text, user_profile, session_context)
    
    def _fallback_response(
        self, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        """Fallback mock response when HF fails"""
        
        # Simple grammar check
        grammar_issues = []
        better_sentence = None
        
        if "go" in user_text.lower() and ("yesterday" in user_text.lower() or "last" in user_text.lower()):
            better_sentence = user_text.replace("go", "went").replace("Go", "Went")
            grammar_issues.append(GrammarFeedback(
                issue="past_tense",
                original_text=user_text,
                explanation_language=user_profile.explanation_language,
                explanation="Gunakan past tense untuk kejadian kemarin" if user_profile.explanation_language == "id" else "Use past tense for yesterday's events",
                examples=["I went to work", "She visited her friend"]
            ))
        
        return MaccaJsonResponse(
            reply=f"That's interesting! You mentioned '{user_text[:30]}...'. Can you tell me more about that?",
            feedback=MaccaFeedback(
                better_sentence=better_sentence,
                grammar=grammar_issues
            ),
            drills=[
                Drill(
                    type="repeat_sentence",
                    instruction="Please repeat this sentence:",
                    sentence=better_sentence
                )
            ] if better_sentence else [],
            next_prompt="Can you tell me more about your day?"
        )