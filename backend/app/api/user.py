from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.schemas.macca import UserProfile, UserProfileUpdate
from app.dependencies import get_current_user_optional, mock_user_profile
from app.db.database import get_db
from app.db.models import User, Session as DBSession, FeedbackIssue

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # If authenticated, return DB user; otherwise return mock for backward compatibility
    if current_user:
        return UserProfile(
            id=str(current_user.id),
            name=current_user.name,
            level=current_user.level,
            goal=current_user.goal,
            explanation_language=current_user.explanation_language,
            common_issues=[]
        )
    return UserProfile(**mock_user_profile)

@router.patch("/profile", response_model=UserProfile)
async def update_user_profile(
    update: UserProfileUpdate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    # If authenticated, update DB user; otherwise update mock
    if current_user:
        if update.name is not None:
            current_user.name = update.name
        if update.level is not None:
            current_user.level = update.level
        if update.goal is not None:
            current_user.goal = update.goal
        if update.explanation_language is not None:
            current_user.explanation_language = update.explanation_language
        
        db.commit()
        db.refresh(current_user)
        
        return UserProfile(
            id=str(current_user.id),
            name=current_user.name,
            level=current_user.level,
            goal=current_user.goal,
            explanation_language=current_user.explanation_language,
            common_issues=[]
        )
    
    # Fallback to mock for backward compatibility
    if update.name is not None:
        mock_user_profile["name"] = update.name
    if update.level is not None:
        mock_user_profile["level"] = update.level
    if update.goal is not None:
        mock_user_profile["goal"] = update.goal
    if update.explanation_language is not None:
        mock_user_profile["explanation_language"] = update.explanation_language
    
    return UserProfile(**mock_user_profile)

@router.get("/progress")
async def get_user_progress(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    # If authenticated, return real progress from DB
    if current_user:
        sessions_count = db.query(DBSession).filter(DBSession.user_id == current_user.id).count()
        total_duration = db.query(func.sum(DBSession.duration_seconds)).filter(
            DBSession.user_id == current_user.id
        ).scalar() or 0
        
        # Get common issues
        common_issues = db.query(
            FeedbackIssue.issue_code,
            func.count(FeedbackIssue.id).label('count')
        ).filter(
            FeedbackIssue.user_id == current_user.id
        ).group_by(FeedbackIssue.issue_code).order_by(func.count(FeedbackIssue.id).desc()).limit(5).all()
        
        return {
            "sessions_completed": sessions_count,
            "total_practice_time_minutes": total_duration // 60,
            "common_issues": [issue[0] for issue in common_issues],
            "vocabulary_learned": db.query(func.count()).select_from(User).filter(User.id == current_user.id).scalar() or 0
        }
    
    # Fallback mock progress for backward compatibility
    return {
        "sessions_completed": 5,
        "total_practice_time_minutes": 45,
        "common_issues": ["past_tense", "articles"],
        "vocabulary_learned": 12
    }