"""Simple Spaced Repetition System (SRS) for vocabulary learning"""

from sqlalchemy.orm import Session as DBSession
from sqlalchemy import or_
from datetime import datetime
from typing import List, Optional
from app.db.models import VocabularyItem

# SRS constants
INITIAL_STRENGTH = 0.2
CORRECT_BOOST = 0.2
INCORRECT_PENALTY = 0.3
MIN_STRENGTH = 0.0
MAX_STRENGTH = 1.0

def get_items_for_review(user_id: str, db: DBSession, limit: int = 5) -> List[VocabularyItem]:
    """Get vocabulary items for review, prioritizing low strength and old reviews
    
    Args:
        user_id: User ID
        db: Database session
        limit: Maximum number of items to return (default 5)
    
    Returns:
        List of VocabularyItem objects sorted by priority (lowest strength first, then oldest review)
    """
    items = db.query(VocabularyItem).filter(
        VocabularyItem.user_id == user_id
    ).order_by(
        VocabularyItem.strength.asc(),
        VocabularyItem.last_reviewed_at.asc().nullsfirst()
    ).limit(limit).all()
    
    return items

def update_review_result(vocabulary_id: str, correct: bool, db: DBSession) -> Optional[VocabularyItem]:
    """Update vocabulary item strength based on review result
    
    Args:
        vocabulary_id: Vocabulary item ID
        correct: Whether the user answered correctly
        db: Database session
    
    Returns:
        Updated VocabularyItem or None if not found
    """
    item = db.query(VocabularyItem).filter(
        VocabularyItem.id == vocabulary_id
    ).first()
    
    if not item:
        return None
    
    # Update strength based on result
    if correct:
        item.strength = min(MAX_STRENGTH, item.strength + CORRECT_BOOST)
    else:
        item.strength = max(MIN_STRENGTH, item.strength - INCORRECT_PENALTY)
    
    # Update last reviewed timestamp
    item.last_reviewed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(item)
    
    return item
