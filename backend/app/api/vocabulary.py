from fastapi import APIRouter, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from app.dependencies import get_current_user_optional, get_current_user
from app.db.database import get_db
from app.db.models import User, VocabularyItem as DBVocabularyItem

router = APIRouter(prefix="/user", tags=["vocabulary"])

class VocabularyItem(BaseModel):
    id: str
    word: str
    translation: str
    example: str
    source: str
    strength: float

class AddVocabularyRequest(BaseModel):
    word: str
    translation: str
    example: str
    source: str = "manual"

# Mock vocabulary for backward compatibility
mock_vocabulary = [
    {
        "id": "vocab_1",
        "word": "experience",
        "translation": "pengalaman",
        "example": "I have five years of experience.",
        "source": "conversation",
        "strength": 0.8
    },
    {
        "id": "vocab_2", 
        "word": "development",
        "translation": "pengembangan",
        "example": "Software development is challenging.",
        "source": "lesson",
        "strength": 0.6
    }
]

@router.get("/vocabulary", response_model=List[VocabularyItem])
async def get_vocabulary(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Get vocabulary items (requires authentication)"""
    items = db.query(DBVocabularyItem).filter(
        DBVocabularyItem.user_id == current_user.id
    ).all()
    return [
        VocabularyItem(
            id=str(item.id),
            word=item.word,
            translation=item.translation,
            example=item.example,
            source=item.source,
            strength=item.strength
        )
        for item in items
    ]

@router.post("/vocabulary", response_model=VocabularyItem)
async def add_vocabulary(
    request: AddVocabularyRequest,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Add vocabulary item (requires authentication)"""
    item = DBVocabularyItem(
        user_id=current_user.id,
        word=request.word,
        translation=request.translation,
        example=request.example,
        source=request.source
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return VocabularyItem(
        id=str(item.id),
        word=item.word,
        translation=item.translation,
        example=item.example,
        source=item.source,
        strength=item.strength
    )