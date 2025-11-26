from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from app.dependencies import get_current_user

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

# Mock vocabulary store
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
async def get_vocabulary(current_user: dict = Depends(get_current_user)):
    return mock_vocabulary

@router.post("/vocabulary", response_model=VocabularyItem)
async def add_vocabulary(
    request: AddVocabularyRequest,
    current_user: dict = Depends(get_current_user)
):
    new_item = {
        "id": f"vocab_{len(mock_vocabulary) + 1}",
        "word": request.word,
        "translation": request.translation,
        "example": request.example,
        "source": "manual",
        "strength": 0.0
    }
    mock_vocabulary.append(new_item)
    return new_item