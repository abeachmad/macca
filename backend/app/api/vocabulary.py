from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession
from datetime import datetime
from app.dependencies import get_current_user_optional, get_current_user
from app.db.database import get_db
from app.db.models import User, VocabularyItem as DBVocabularyItem
from app.services import srs

router = APIRouter(prefix="/user", tags=["vocabulary"])

class VocabularyItem(BaseModel):
    id: str
    word: str
    translation: str
    example: str
    source: str
    strength: float
    last_reviewed_at: Optional[datetime] = None

class AddVocabularyRequest(BaseModel):
    word: str
    translation: str
    example: str
    source: str = "manual"

class ReviewNextResponse(BaseModel):
    items: List[VocabularyItem]

class ReviewAnswerRequest(BaseModel):
    vocabulary_id: str
    correct: bool

class ReviewAnswerResponse(BaseModel):
    item: VocabularyItem
    message: str

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
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    """Get vocabulary items
    
    Backward compatibility: Returns mock data if no auth provided.
    This is transitional - future versions may enforce strict auth.
    """
    if current_user:
        # Authenticated: return DB vocabulary
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
                strength=item.strength,
                last_reviewed_at=item.last_reviewed_at
            )
            for item in items
        ]
    
    # No auth: return empty list for backward compatibility
    return []

@router.post("/vocabulary", response_model=VocabularyItem)
async def add_vocabulary(
    request: AddVocabularyRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: DBSession = Depends(get_db)
):
    """Add vocabulary item
    
    Backward compatibility: Returns mock response if no auth provided.
    This is transitional - future versions may enforce strict auth.
    """
    if current_user:
        # Authenticated: save to DB with initial SRS strength
        item = DBVocabularyItem(
            user_id=current_user.id,
            word=request.word,
            translation=request.translation,
            example=request.example,
            source=request.source,
            strength=srs.INITIAL_STRENGTH
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
            strength=item.strength,
            last_reviewed_at=item.last_reviewed_at
        )
    
    # No auth: return mock response for backward compatibility (not persisted)
    return VocabularyItem(
        id="temp_" + request.word,
        word=request.word,
        translation=request.translation,
        example=request.example,
        source=request.source,
        strength=0.0,
        last_reviewed_at=None
    )

@router.post("/vocabulary/review/next", response_model=ReviewNextResponse)
async def get_vocabulary_for_review(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Get vocabulary items for review (SRS-based)
    
    Returns items prioritized by:
    - Lowest strength first (items that need more practice)
    - Longest time since last review
    
    Auth required: Returns 401 if no valid token provided.
    """
    items = srs.get_items_for_review(current_user.id, db, limit=limit)
    
    return ReviewNextResponse(
        items=[
            VocabularyItem(
                id=str(item.id),
                word=item.word,
                translation=item.translation,
                example=item.example,
                source=item.source,
                strength=item.strength,
                last_reviewed_at=item.last_reviewed_at
            )
            for item in items
        ]
    )

@router.post("/vocabulary/review/answer", response_model=ReviewAnswerResponse)
async def submit_vocabulary_review(
    request: ReviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Submit vocabulary review answer and update SRS strength
    
    Updates item strength:
    - Correct: +0.2 (capped at 1.0)
    - Incorrect: -0.3 (floored at 0.0)
    
    Auth required: Returns 401 if no valid token provided.
    """
    item = srs.update_review_result(request.vocabulary_id, request.correct, db)
    
    if not item:
        raise HTTPException(status_code=404, detail="Vocabulary item not found")
    
    # Verify ownership
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    
    message = "Great! Keep practicing." if request.correct else "Don't worry, practice makes perfect!"
    
    return ReviewAnswerResponse(
        item=VocabularyItem(
            id=str(item.id),
            word=item.word,
            translation=item.translation,
            example=item.example,
            source=item.source,
            strength=item.strength,
            last_reviewed_at=item.last_reviewed_at
        ),
        message=message
    )