# Quick Start Guide - Macca Backend

## Development Mode (Mock AI)

```bash
cd backend

# 1. Create .env file
cp .env.example .env

# 2. Edit .env - set USE_MOCK_AI=true
USE_MOCK_AI=true
DATABASE_URL=sqlite:///./dev.db

# 3. Run tests
export PYTHONPATH=venv/lib/python3.12/site-packages:$PYTHONPATH
python3 test_api.py

# 4. Start server
./start.sh
# Or: uvicorn app.main:app --reload
```

## Production Mode (Real HuggingFace)

```bash
cd backend

# 1. Set up PostgreSQL
createdb macca

# 2. Edit .env
USE_MOCK_AI=false
HF_API_KEY=your_huggingface_token_here
DATABASE_URL=postgresql://user:pass@localhost/macca

# 3. Run migrations
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head

# 4. Start server
./start.sh
```

## Audio Endpoints (New in Batch 2)

```bash
# Audio-based conversation turn
curl -X POST http://localhost:8000/api/session/turn/audio \
  -F "audio=@recording.wav" \
  -F "mode=live" \
  -F "session_id=sess_123"

# Audio-based pronunciation analysis
curl -X POST http://localhost:8000/api/pronunciation/analyze/audio \
  -F "audio=@recording.wav" \
  -F "word=think"
```

## Environment Variables

```bash
# AI Provider Mode
USE_MOCK_AI=true              # true = mock, false = HuggingFace

# HuggingFace (only needed if USE_MOCK_AI=false)
HF_API_KEY=hf_xxxxx
HF_LLM_MODEL_ID=SeaLLMs/SeaLLMs-v3-7B-Chat
HF_ASR_MODEL_ID=openai/whisper-large-v3-turbo
HF_TTS_MODEL_ID=audo/seamless-m4t-v2-large

# Database
DATABASE_URL=postgresql://localhost/macca

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

## Testing

```bash
# Run API tests (uses SQLite + mock AI)
python3 test_api.py

# Run JSON parsing tests
python3 test_llm_parsing.py

# Both should show all tests passing
```

## Logs

When server starts, you'll see:
```
🤖 AI Provider Mode: MOCK (USE_MOCK_AI=true or HF_API_KEY not set)
```

Or in production:
```
🤖 AI Provider Mode: HUGGING FACE (Model: SeaLLMs/SeaLLMs-v3-7B-Chat)
```

## API Endpoints

### Public Endpoints (No Auth Required)
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/user/profile` - Get profile (mock if no auth)
- `PATCH /api/user/profile` - Update profile (mock if no auth)
- `GET /api/user/progress` - Get learning progress (mock if no auth)
- `POST /api/session/start` - Start session
- `POST /api/session/turn` - Process conversation (text)
- `POST /api/pronunciation/analyze` - Analyze pronunciation (text)
- `GET /api/lessons` - List lessons
- `GET /api/lessons/{id}` - Get lesson

### Auth Required Endpoints
- `GET /api/user/vocabulary` - Get vocabulary (requires JWT)
- `POST /api/user/vocabulary` - Add vocabulary (requires JWT)

### Audio Endpoints (New)
- `POST /api/session/turn/audio` - Process conversation with audio
- `POST /api/pronunciation/analyze/audio` - Analyze pronunciation with audio

## Troubleshooting

**Tests fail with database error:**
- Make sure `DATABASE_URL` in test uses SQLite: `sqlite:///./test.db`

**HuggingFace errors in production:**
- Check `HF_API_KEY` is valid
- Check model IDs are correct
- Providers will fallback to mock responses on error

**Audio files not saving:**
- Check `storage/audio` directory exists and is writable
- Check StaticFiles mount in `main.py`

## Documentation

- `DATABASE.md` - Database setup and migrations
- `PROVIDER_IMPROVEMENTS.md` - Provider implementation details
- `BATCH1_SUMMARY.md` - Complete feature summary
- `CHANGES.md` - All changes from previous sessions
