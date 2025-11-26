# Macca – AI English Speaking Coach

> **Macca** is an AI English speaking coach for Indonesian learners, focused on **speaking & listening** practice with short, real-time, personalized feedback.

## Quick Start

### Backend Setup

1. **Install dependencies:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start the backend:**
   ```bash
   ./start.sh
   # Or manually: uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the frontend:**
   ```bash
   npm start
   ```

## Architecture

### Backend (Python/FastAPI)
- **Modular structure** with separate routers, services, and providers
- **Mock AI providers** for development (set `USE_MOCK_AI=true`)
- **PostgreSQL** database with SQLAlchemy models
- **Hugging Face integration** ready for ASR, LLM, and TTS

### Frontend (React)
- **Modern UI** with Tailwind CSS and shadcn/ui components
- **Voice-first design** with microphone as primary CTA
- **Real-time feedback** display and conversation history

## Learning Modes

1. **Live Conversation** - Free conversation with structured feedback
2. **Guided Lessons** - Structured tasks with lesson progression  
3. **Pronunciation Coach** - Focused practice on specific sounds

## API Endpoints

- `GET /api/user/profile` - Get user profile
- `PATCH /api/user/profile` - Update user profile
- `POST /api/session/turn` - Process conversation turn
- `POST /api/pronunciation/analyze` - Analyze pronunciation
- `GET /api/lessons` - Get available lessons
- `GET /api/lessons/{id}` - Get specific lesson

## Development

### Testing
```bash
cd backend
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run API tests
python test_api.py

# Test with real Hugging Face (set HF_API_KEY first)
export USE_MOCK_AI=false
python test_api.py
```

### Database Migrations
```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Configuration

Key environment variables:
- `USE_MOCK_AI=true` - Use mock providers for development
- `HF_API_KEY` - Hugging Face API key (required when USE_MOCK_AI=false)
- `HF_LLM_MODEL_ID` - Hugging Face LLM model ID
- `HF_ASR_MODEL_ID` - Hugging Face ASR model ID  
- `HF_TTS_MODEL_ID` - Hugging Face TTS model ID
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed CORS origins

## Features

### ✅ Implemented
- **Modular FastAPI Architecture** - Clean separation of concerns
- **Mock AI Providers** - Full development environment without external APIs
- **Real Hugging Face Integration** - Ready for production AI services
- **JWT Authentication** - User signup/login with secure tokens
- **Structured Feedback System** - Grammar, vocabulary, and pronunciation feedback
- **Session Management** - Track learning sessions and progress
- **Vocabulary Management** - Add and track vocabulary items
- **Storage Service** - Audio file handling with static serving
- **Database Models** - PostgreSQL schema with SQLAlchemy
- **API Testing** - Comprehensive test suite

### 🔄 Ready for Extension
- **Audio Processing** - ASR and TTS providers ready for audio input/output
- **Database Persistence** - Models defined, migrations ready
- **Real-time Feedback** - Structured response format for frontend
- **Multi-language Support** - Indonesian/English explanation system