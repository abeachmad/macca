#!/usr/bin/env python3
"""
Auto-cleanup script for temporary TTS audio files.
Deletes audio files older than 1 hour.
Run this as a cron job: */30 * * * * /path/to/cleanup_audio.py
"""
import os
import time
from pathlib import Path

AUDIO_DIR = Path(__file__).parent / "storage" / "audio"
MAX_AGE_SECONDS = 3600  # 1 hour

def cleanup_old_audio():
    if not AUDIO_DIR.exists():
        return
    
    now = time.time()
    deleted = 0
    
    for audio_file in AUDIO_DIR.glob("*.mp3"):
        if now - audio_file.stat().st_mtime > MAX_AGE_SECONDS:
            audio_file.unlink()
            deleted += 1
    
    if deleted > 0:
        print(f"Deleted {deleted} old audio files")

if __name__ == "__main__":
    cleanup_old_audio()
