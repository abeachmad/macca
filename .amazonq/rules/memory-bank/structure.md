# Project Structure

## Directory Organization

```
macca/
├── backend/              # Python FastAPI backend server
│   ├── app/
│   │   ├── api/         # API route handlers (routers)
│   │   ├── db/          # Database models and connection
│   │   ├── providers/   # AI service providers (ASR, LLM, TTS)
│   │   ├── schemas/     # Pydantic request/response schemas
│   │   ├── services/    # Business logic layer
│   │   ├── config.py    # Configuration management
│   │   ├── dependencies.py  # FastAPI dependency injection
│   │   └── main.py      # Application entry point
│   ├── storage/
│   │   └── audio/       # Audio file storage
│   ├── requirements.txt # Python dependencies
│   ├── start.sh         # Backend startup script
│   └── test_*.py        # Test files
├── frontend/            # React frontend application
│   ├── plugins/         # Build and development plugins
│   │   ├── health-check/    # Health monitoring plugin
│   │   └── visual-edits/    # Visual editing tools
│   ├── public/          # Static assets
│   ├── src/
│   │   ├── components/  # Reusable UI components
│   │   ├── context/     # React context providers
│   │   ├── hooks/       # Custom React hooks
│   │   ├── lib/         # Utility libraries
│   │   ├── pages/       # Page components (routes)
│   │   ├── App.jsx      # Main application component
│   │   └── index.jsx    # Application entry point
│   ├── package.json     # Node dependencies
│   └── vite.config.js   # Vite build configuration
├── logs/                # Application logs
├── tests/               # Shared test utilities
└── dev-*.sh             # Development scripts
```

## Core Components

### Backend Architecture

**Layered Architecture Pattern:**
1. **API Layer** (`app/api/`): Route handlers that receive HTTP requests
2. **Service Layer** (`app/services/`): Business logic and orchestration
3. **Provider Layer** (`app/providers/`): External service integrations (AI models)
4. **Data Layer** (`app/db/`): Database models and persistence

**Key Backend Components:**
- **Routers**: Handle HTTP endpoints for user, session, pronunciation, lessons
- **Services**: Orchestrate business logic (feedback generation, session management)
- **Providers**: Abstract AI services with mock and real implementations
  - `MockLLMProvider` / `HuggingFaceLLMProvider`
  - `MockASRProvider` / `HuggingFaceASRProvider`
  - `MockTTSProvider` / `HuggingFaceTTSProvider`
- **Models**: SQLAlchemy ORM models for User, Session, Turn, Vocabulary, Lesson
- **Schemas**: Pydantic models for request validation and response serialization

### Frontend Architecture

**Component-Based Architecture:**
- **Pages**: Top-level route components (LiveConversation, GuidedLessons, PronunciationCoach)
- **Components**: Reusable UI elements built with shadcn/ui and Radix UI
- **Context**: Global state management (AuthContext for user authentication)
- **Hooks**: Custom React hooks for API calls and shared logic
- **Lib**: Utility functions and helpers

**Key Frontend Components:**
- **Voice Interface**: Microphone input and audio recording
- **Feedback Display**: Real-time display of grammar, vocabulary, pronunciation feedback
- **Session History**: Conversation turn tracking and replay
- **Lesson Browser**: Guided lesson selection and progress tracking

## Architectural Patterns

### Backend Patterns
- **Dependency Injection**: FastAPI's dependency system for database sessions and services
- **Provider Pattern**: Swappable AI providers (mock vs. real) via configuration
- **Repository Pattern**: Database access abstracted through SQLAlchemy models
- **DTO Pattern**: Pydantic schemas separate API contracts from internal models
- **Service Layer**: Business logic isolated from HTTP concerns

### Frontend Patterns
- **Component Composition**: Small, reusable components composed into pages
- **Context API**: Global state for authentication and user data
- **Custom Hooks**: Encapsulate API calls and stateful logic
- **Utility-First CSS**: Tailwind CSS for styling
- **Route-Based Code Splitting**: Vite handles lazy loading of page components

## Data Flow

### Conversation Turn Flow
1. User speaks → Frontend captures audio
2. Audio sent to `/api/session/turn` endpoint
3. Backend ASR provider transcribes audio to text
4. LLM provider generates response and feedback
5. TTS provider converts response to audio
6. Structured response returned to frontend
7. Frontend displays feedback and plays audio response

### Authentication Flow
1. User signs up/logs in via `/api/auth/` endpoints
2. Backend generates JWT token
3. Frontend stores token in AuthContext
4. Token included in subsequent API requests
5. Backend validates token via dependency injection

## Configuration Management
- **Environment Variables**: `.env` files for backend and frontend
- **Config Module**: `app/config.py` centralizes backend configuration
- **Feature Flags**: `USE_MOCK_AI` toggles between mock and real AI providers
- **CORS Configuration**: Configurable allowed origins for API access
