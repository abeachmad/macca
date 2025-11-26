from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/live")
async def liveness():
    """Liveness probe - always returns 200 if app is running"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "use_mock_ai": settings.use_mock_ai
    }

@router.get("/ready")
async def readiness(db: Session = Depends(get_db)):
    """Readiness probe - checks DB connection"""
    try:
        # Test DB connection with lightweight query
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "database": "error",
            "use_mock_ai": settings.use_mock_ai
        }, 503
    
    return {
        "status": "ok",
        "database": db_status,
        "use_mock_ai": settings.use_mock_ai
    }
