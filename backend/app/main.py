from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import logging

from app.config import settings
from app.api import user, session, pronunciation, lessons, auth, vocabulary, health

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Macca API", description="AI English Speaking Coach")

# Startup configuration validation
def validate_startup_config():
    """Validate configuration at startup and fail fast if misconfigured"""
    logger.info("="*50)
    logger.info("Macca API Starting")
    logger.info(f"USE_MOCK_AI: {settings.use_mock_ai}")
    
    if settings.use_mock_ai:
        logger.info("AI Provider: MOCK (no external API calls)")
    else:
        logger.info("AI Provider: HYBRID (Groq LLM + HuggingFace Audio)")
        if settings.groq_api_key:
            logger.info(f"  LLM: Groq ({settings.groq_model_id})")
        else:
            logger.warning("  LLM: MOCK (GROQ_API_KEY not set)")
        
        if settings.hf_api_key:
            logger.info(f"  ASR: HuggingFace ({settings.hf_asr_model_id})")
            logger.info(f"  TTS: HuggingFace ({settings.hf_tts_model_id})")
        else:
            logger.warning("  ASR/TTS: MOCK (HF_API_KEY not set)")
    
    logger.info(f"Database: {settings.database_url.split('@')[-1] if '@' in settings.database_url else settings.database_url}")
    logger.info(f"Log Level: {log_level}")
    logger.info("="*50)

validate_startup_config()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=settings.cors_origins.split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create storage directory and mount static files
storage_dir = Path("./storage")
storage_dir.mkdir(exist_ok=True)
audio_dir = storage_dir / "audio"
audio_dir.mkdir(exist_ok=True)

app.mount("/static", StaticFiles(directory="storage"), name="static")

# Include routers
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(session.router, prefix="/api")
app.include_router(pronunciation.router, prefix="/api")
app.include_router(vocabulary.router, prefix="/api")
app.include_router(lessons.router, prefix="/api")

@app.get("/api/")
async def root():
    return {"message": "Macca API - Modular Backend"}

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Macca API is running"}

# Add to backend/app/main.py
from fastapi.responses import FileResponse

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico", status_code=404)
