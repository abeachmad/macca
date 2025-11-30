# Development Guidelines

## Code Quality Standards

### Python Backend Standards

**Import Organization:**
- Standard library imports first
- Third-party imports second
- Local application imports last
- Group imports logically (e.g., FastAPI, SQLAlchemy, app modules)
```python
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session as DBSession
from datetime import datetime
import uuid
import logging

from app.schemas.macca import ConversationTurn, ConversationResponse
from app.providers.base import LLMProvider, TTSProvider, ASRProvider
from app.dependencies import get_llm_provider, get_tts_provider
from app.db.database import get_db
from app.db.models import User, Session, Utterance
```

**Naming Conventions:**
- Classes: PascalCase (e.g., `HuggingFaceLLMProvider`, `UserProfile`)
- Functions/methods: snake_case (e.g., `generate_macca_response`, `process_conversation_turn`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_AUDIO_SIZE`, `ARRAY_METHODS`)
- Private methods: prefix with underscore (e.g., `_build_system_prompt`, `_parse_llm_response`)
- Database aliases: Use descriptive aliases (e.g., `Session as DBSession` to avoid conflicts)

**Logging:**
- Use module-level logger: `logger = logging.getLogger(__name__)`
- Log at appropriate levels: INFO for operations, WARNING for fallbacks, ERROR for failures
- Include context in log messages (user_id, session_id, file sizes, status codes)
```python
logger.info(f"POST /session/turn/audio - user_id={user_id}, session_id={session_id}")
logger.warning(f"HF LLM API returned status {response.status_code}: {response.text[:200]}")
logger.error(f"Unexpected error in HF LLM provider: {e}")
```

**Type Hints:**
- Use type hints for all function parameters and return values
- Use `Optional[Type]` for nullable values
- Use `List[Type]` for lists with specific types
```python
async def generate_macca_response(
    self, 
    user_text: str, 
    user_profile: UserProfile, 
    session_context: SessionContext
) -> MaccaJsonResponse:
```

**Docstrings:**
- Use triple-quoted strings for function/class documentation
- Keep docstrings concise and descriptive
```python
def process_conversation_turn_audio():
    """Process conversation turn with audio input"""
```

### JavaScript/React Frontend Standards

**Import Organization:**
- React imports first
- Third-party library imports second
- Local component imports third
- Local utility/context imports last
- Use `@/` alias for src directory imports
```javascript
import React, { useState } from 'react';
import Layout from '@/components/Layout';
import LearnerContextBar from '@/components/LearnerContextBar';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useMacca } from '@/context/MaccaContext';
import { Mic, Volume2 } from 'lucide-react';
```

**Naming Conventions:**
- Components: PascalCase (e.g., `PronunciationCoach`, `LearnerContextBar`)
- Functions/variables: camelCase (e.g., `handlePracticeWord`, `selectedSound`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_AUDIO_SIZE`, `EXTENSIONS`)
- Event handlers: prefix with `handle` (e.g., `handlePracticeWord`, `onClick`)
- Boolean variables: prefix with `is/has` (e.g., `isRecording`, `hasDebugAttr`)

**Component Structure:**
- Functional components with hooks
- State declarations at the top
- Helper functions in the middle
- Return JSX at the bottom
```javascript
const PronunciationCoach = () => {
  const { analyzePronunciation, userProfile } = useMacca();
  const [selectedSound, setSelectedSound] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  
  const handlePracticeWord = async (word) => {
    // Implementation
  };
  
  return (
    <Layout>
      {/* JSX */}
    </Layout>
  );
};
```

**Conditional Styling:**
- Use template literals for dynamic classes
- Use ternary operators for conditional classes
- Combine Tailwind classes with utility functions when needed
```javascript
className={`cursor-pointer transition-all ${
  selectedSound?.id === item.id
    ? 'bg-cyan-500/20 border-cyan-500'
    : 'bg-slate-800/50 border-slate-700 hover:border-cyan-500/50'
}`}
```

## Architectural Patterns

### Backend Patterns

**Dependency Injection:**
- Use FastAPI's `Depends()` for service injection
- Inject database sessions, providers, and current user
```python
async def process_conversation_turn(
    turn: ConversationTurn,
    llm_provider: LLMProvider = Depends(get_llm_provider),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
```

**Provider Pattern:**
- Abstract external services behind provider interfaces
- Implement both mock and real providers
- Use configuration to switch between providers
```python
class HuggingFaceLLMProvider:
    def __init__(self):
        self.api_key = settings.hf_api_key
        self.model_id = settings.hf_llm_model_id
    
    async def generate_macca_response(...) -> MaccaJsonResponse:
        # Implementation
```

**Error Handling:**
- Use try-except blocks for external API calls
- Provide fallback responses when services fail
- Log errors with context
- Raise HTTPException for client errors
```python
try:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            logger.warning(f"API returned status {response.status_code}")
            return self._fallback_response(...)
except (httpx.TimeoutException, httpx.RequestError) as e:
    logger.error(f"API request failed: {e}")
    return self._fallback_response(...)
```

**Database Operations:**
- Use SQLAlchemy ORM for database access
- Commit after all related operations
- Refresh objects after commit to get generated IDs
```python
session = Session(user_id=current_user.id, mode=request.mode)
db.add(session)
db.commit()
db.refresh(session)
```

**Response Formatting:**
- Use Pydantic models for request/response validation
- Convert internal models to API response models
- Maintain backward compatibility with legacy formats
```python
return ConversationResponse(
    macca_text=macca_response.reply,
    feedback=feedback,
    next_step="step_3" if turn.mode == "guided" else None
)
```

### Frontend Patterns

**State Management:**
- Use React hooks (useState, useEffect) for local state
- Use Context API for global state (authentication, user profile)
- Lift state up when shared between components
```javascript
const { analyzePronunciation, userProfile } = useMacca();
const [selectedSound, setSelectedSound] = useState(null);
```

**Async Operations:**
- Use async/await for API calls
- Show loading states during operations
- Handle errors with try-catch
```javascript
const handlePracticeWord = async (word) => {
  setIsRecording(true);
  try {
    const result = await analyzePronunciation(word);
    setFeedback(result);
  } catch (error) {
    console.error('Error analyzing:', error);
  } finally {
    setIsAnalyzing(false);
  }
};
```

**Conditional Rendering:**
- Use ternary operators for simple conditions
- Use logical AND (&&) for conditional display
- Extract complex conditions into helper functions
```javascript
{selectedSound ? (
  <div className="space-y-4">
    {/* Content */}
  </div>
) : (
  <Card>
    <p>Select a sound to start practicing</p>
  </Card>
)}
```

**Component Composition:**
- Break down complex UIs into smaller components
- Use shadcn/ui components as building blocks
- Pass data via props, callbacks via event handlers
```javascript
<Card className="bg-slate-800/50 border-slate-700">
  <CardHeader>
    <CardTitle>Practice: {selectedSound.name}</CardTitle>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>
```

## Common Implementation Patterns

### API Endpoint Pattern (Backend)
```python
@router.post("/endpoint", response_model=ResponseModel)
async def endpoint_handler(
    request: RequestModel,
    service: ServiceType = Depends(get_service),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    # 1. Build context from user and request
    # 2. Call service layer
    # 3. Persist to database if authenticated
    # 4. Return formatted response
```

### LLM Response Parsing Pattern (Backend)
```python
def _parse_llm_response(self, generated_text: str, ...) -> MaccaJsonResponse:
    # 1. Extract JSON from text using regex
    json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
    
    # 2. Parse and validate JSON
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            return MaccaJsonResponse(...)
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to parse: {e}")
    
    # 3. Fallback to mock response
    return self._fallback_response(...)
```

### Dynamic Detection Pattern (Frontend Plugin)
```javascript
// 1. Check cache first
if (CACHE.has(cacheKey)) return CACHE.get(cacheKey);

// 2. Parse file AST
const ast = parseFileAst(absPath, parser);

// 3. Traverse AST to detect patterns
traverse(ast, {
  NodeType(path) {
    // Detection logic
  }
});

// 4. Cache result
CACHE.set(cacheKey, result);
return result;
```

### Form Handling Pattern (Frontend)
```javascript
// 1. Capture user input
const input = document.getElementById('input-id');
const value = input.value || defaultValue;

// 2. Set loading state
setIsLoading(true);

// 3. Call API
try {
  const result = await apiCall(value);
  setResult(result);
} catch (error) {
  console.error('Error:', error);
} finally {
  setIsLoading(false);
}
```

## Frequently Used Code Idioms

### Backend Idioms

**Optional User Authentication:**
```python
if current_user:
    # Authenticated flow with database persistence
    user_profile = UserProfile(
        id=str(current_user.id),
        name=current_user.name,
        level=current_user.level
    )
else:
    # Anonymous flow with mock data
    from app.dependencies import mock_user_profile
    user_profile = UserProfile(**mock_user_profile)
```

**File Upload Validation:**
```python
audio_bytes = await audio.read()
if len(audio_bytes) > MAX_AUDIO_SIZE:
    raise HTTPException(
        status_code=413,
        detail=f"File too large (max {MAX_AUDIO_SIZE // (1024*1024)} MB)"
    )
```

**UUID Generation:**
```python
# In models
id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

# In code
session_id = f"sess_{uuid.uuid4().hex[:8]}"
```

### Frontend Idioms

**Conditional Class Application:**
```javascript
className={`base-classes ${condition ? 'true-classes' : 'false-classes'}`}
```

**Array Mapping with Index:**
```javascript
{items.map((item, index) => (
  <Component key={index} {...item} />
))}
```

**Switch-Case for Styling:**
```javascript
const getColor = (status) => {
  switch (status) {
    case 'success': return 'bg-green-500';
    case 'warning': return 'bg-yellow-500';
    case 'error': return 'bg-red-500';
    default: return 'bg-slate-500';
  }
};
```

**Optional Chaining:**
```javascript
const value = object?.property?.nestedProperty || defaultValue;
```

## Configuration Management

**Environment Variables:**
- Use `.env` files for configuration
- Never commit `.env` files (use `.env.example` as template)
- Access via `settings` object in backend, `process.env` in frontend
```python
# Backend
from app.config import settings
api_key = settings.hf_api_key

# Frontend
const apiUrl = process.env.REACT_APP_API_URL;
```

**Feature Flags:**
- Use boolean flags for toggling features
- Check flags at initialization
```python
if settings.use_mock_ai:
    return MockLLMProvider()
else:
    return HuggingFaceLLMProvider()
```

## Testing Patterns

**API Testing:**
- Test with mock providers first
- Test with real providers when API keys available
- Log request/response for debugging
```python
# Run with mock
export USE_MOCK_AI=true
python test_api.py

# Run with real API
export USE_MOCK_AI=false
python test_api.py
```

## Performance Considerations

**Caching:**
- Cache expensive computations (file parsing, AST traversal)
- Use WeakMap/WeakSet for node-based caching to prevent memory leaks
- Clear caches when appropriate
```javascript
const CACHE = new Map();
const NODE_CACHE = new WeakMap();
```

**Async Operations:**
- Use async/await for I/O operations
- Set appropriate timeouts for external API calls
- Handle timeouts gracefully with fallbacks
```python
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.post(...)
```

**Database Queries:**
- Use eager loading for relationships when needed
- Order by timestamp descending for recent items
- Limit query results when appropriate
```python
session = db.query(Session).filter(
    Session.user_id == current_user.id
).order_by(Session.started_at.desc()).first()
```
