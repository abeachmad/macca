from fastapi import APIRouter, Depends
from app.schemas.macca import UserProfile, UserProfileUpdate
from app.dependencies import mock_user_profile

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=UserProfile)
async def get_user_profile():
    return UserProfile(**mock_user_profile)

@router.patch("/profile", response_model=UserProfile)
async def update_user_profile(update: UserProfileUpdate):
    # Update mock profile
    if update.name is not None:
        mock_user_profile["name"] = update.name
    if update.level is not None:
        mock_user_profile["level"] = update.level
    if update.goal is not None:
        mock_user_profile["goal"] = update.goal
    if update.explanation_language is not None:
        mock_user_profile["explanation_language"] = update.explanation_language
    
    return UserProfile(**mock_user_profile)