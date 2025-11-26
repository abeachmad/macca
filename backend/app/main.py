from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from app.config import settings
from app.api import user, session, pronunciation, lessons, auth, vocabulary

# Create FastAPI app
app = FastAPI(title="Macca API", description="AI English Speaking Coach")

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