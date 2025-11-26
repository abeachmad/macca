import os
import uuid
from pathlib import Path

class StorageService:
    def __init__(self, storage_dir: str = "./storage"):
        self.storage_dir = Path(storage_dir)
        self.audio_dir = self.storage_dir / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    def save_audio(self, file_bytes: bytes, extension: str = "wav") -> str:
        """Save audio file and return URL"""
        filename = f"{uuid.uuid4()}.{extension}"
        file_path = self.audio_dir / filename
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        return f"/static/audio/{filename}"