import httpx
import json
import logging
from typing import Optional
from app.providers.base import LLMProvider
from app.schemas.macca import UserProfile, SessionContext, MaccaJsonResponse
from app.config import settings

logger = logging.getLogger(__name__)

class GroqLLMProvider(LLMProvider):
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model_id = settings.groq_model_id
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def _build_system_prompt(self, user_profile: UserProfile, session_context: SessionContext) -> str:
        mode = session_context.mode
        
        base_prompt = f"""You are Macca, an AI English speaking coach for Indonesian learners.

User Profile:
- Name: {user_profile.name}
- Level: {user_profile.level}
- Native Language: Indonesian

Mode: {mode}

Your response MUST be valid JSON with this structure:
{{
  "reply": "your conversational response in English",
  "grammar_feedback": [{{"issue": "...", "correction": "...", "explanation": "..."}}],
  "vocabulary_feedback": [{{"word": "...", "suggestion": "...", "explanation": "..."}}],
  "pronunciation_feedback": [{{"word": "...", "tip": "..."}}]
}}

IMPORTANT: Always respond in ENGLISH. Keep replies natural and conversational."""

        if mode == "live":
            base_prompt += "\n\nLive Mode: Have natural conversations. Provide feedback after each turn."
        elif mode == "guided":
            base_prompt += f"\n\nGuided Mode: Current task: {session_context.current_task or 'General practice'}. Guide the learner through structured exercises."
        
        return base_prompt
    
    async def generate_macca_response(
        self, 
        user_text: str, 
        user_profile: UserProfile, 
        session_context: SessionContext
    ) -> MaccaJsonResponse:
        system_prompt = self._build_system_prompt(user_profile, session_context)
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
        
        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
            "response_format": {"type": "json_object"}
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.api_url, json=payload, headers=headers)
                
                if response.status_code != 200:
                    logger.error(f"Groq API error {response.status_code}: {response.text}")
                    raise Exception(f"Groq API returned {response.status_code}")
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                data = json.loads(content)
                return MaccaJsonResponse(
                    reply=data.get("reply", "I'm here to help you practice English!"),
                    grammar_feedback=data.get("grammar_feedback", []),
                    vocabulary_feedback=data.get("vocabulary_feedback", []),
                    pronunciation_feedback=data.get("pronunciation_feedback", [])
                )
        
        except Exception as e:
            logger.error(f"Groq LLM error: {e}")
            raise
