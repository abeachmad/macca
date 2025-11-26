from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.schemas.macca import UserProfile, UserProfileUpdate
from app.dependencies import get_current_user_optional, mock_user_profile
from app.db.database import get_db
from app.db.models import User, Session as DBSession, FeedbackIssue, Utterance, VocabularyItem as DBVocabularyItem

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
        # Basic counts
        total_sessions = db.query(DBSession).filter(DBSession.user_id == current_user.id).count()
        total_utterances = db.query(Utterance).filter(Utterance.user_id == current_user.id).count()
        vocabulary_count = db.query(DBVocabularyItem).filter(DBVocabularyItem.user_id == current_user.id).count()
        
        # Total practice time
        total_duration = db.query(func.sum(DBSession.duration_seconds)).filter(
            DBSession.user_id == current_user.id
        ).scalar() or 0
        
        # Top grammar issues with counts
        grammar_issues = db.query(
            FeedbackIssue.issue_code,
            func.count(FeedbackIssue.id).label('count')
        ).filter(
            FeedbackIssue.user_id == current_user.id,
            FeedbackIssue.type == 'grammar'
        ).group_by(FeedbackIssue.issue_code).order_by(func.count(FeedbackIssue.id).desc()).limit(5).all()
        
        # All common issues (for backward compatibility)
        all_issues = db.query(
            FeedbackIssue.issue_code
        ).filter(
            FeedbackIssue.user_id == current_user.id
        ).group_by(FeedbackIssue.issue_code).order_by(func.count(FeedbackIssue.id).desc()).limit(5).all()
        
        return {
            # Backward compatible fields
            "sessions_completed": total_sessions,
            "total_practice_time_minutes": total_duration // 60,
            "common_issues": [issue[0] for issue in all_issues],
            "vocabulary_learned": vocabulary_count,
            
            # New analytics fields (additive, optional)
            "total_sessions": total_sessions,
            "total_utterances": total_utterances,
            "total_practice_seconds": total_duration,
            "top_grammar_issues": [
                {"issue_code": issue[0], "count": issue[1]}
                for issue in grammar_issues
            ],
            "vocabulary_items_count": vocabulary_count
        }
    
    # Fallback mock progress for backward compatibility
    return {
        "sessions_completed": 5,
        "total_practice_time_minutes": 45,
        "common_issues": ["past_tense", "articles"],
        "vocabulary_learned": 12
    }