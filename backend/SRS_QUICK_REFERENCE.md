# SRS Quick Reference

## Overview
Simple Spaced Repetition System for vocabulary learning in Macca.

## Constants (app/services/srs.py)
```python
INITIAL_STRENGTH = 0.2      # New items
CORRECT_BOOST = 0.2         # +0.2 on correct
INCORRECT_PENALTY = 0.3     # -0.3 on incorrect
MIN_STRENGTH = 0.0          # Floor
MAX_STRENGTH = 1.0          # Ceiling
```

## API Endpoints

### Get Items for Review
```bash
POST /api/user/vocabulary/review/next?limit=5
Authorization: Bearer <token>
```

**Response**:
```json
{
  "items": [
    {
      "id": "vocab_123",
      "word": "experience",
      "translation": "pengalaman",
      "example": "I have five years of experience.",
      "source": "conversation",
      "strength": 0.2,
      "last_reviewed_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Submit Review Answer
```bash
POST /api/user/vocabulary/review/answer
Authorization: Bearer <token>
Content-Type: application/json

{
  "vocabulary_id": "vocab_123",
  "correct": true
}
```

**Response**:
```json
{
  "item": {
    "id": "vocab_123",
    "word": "experience",
    "strength": 0.4,
    "last_reviewed_at": "2024-01-15T11:00:00Z",
    ...
  },
  "message": "Great! Keep practicing."
}
```

## Strength Progression

| Current | Correct → | Incorrect → |
|---------|-----------|-------------|
| 0.0     | 0.2       | 0.0         |
| 0.2     | 0.4       | 0.0         |
| 0.4     | 0.6       | 0.1         |
| 0.6     | 0.8       | 0.3         |
| 0.8     | 1.0       | 0.5         |
| 1.0     | 1.0       | 0.7         |

## Review Priority

Items returned in this order:
1. Lowest strength first
2. Oldest last_reviewed_at (NULL first)
3. Limited to requested count

## Python Usage

```python
from app.services import srs

# Get items
items = srs.get_items_for_review(user_id, db, limit=5)

# Update result
item = srs.update_review_result(vocab_id, correct=True, db)
```

## Frontend Example

```typescript
// Get review items
const { items } = await api.post('/user/vocabulary/review/next');

// Show flashcard
const item = items[0];
showFlashcard(item.word, item.translation, item.example);

// Submit answer
const { item: updated, message } = await api.post(
  '/user/vocabulary/review/answer',
  { vocabulary_id: item.id, correct: userWasCorrect }
);

console.log(message); // "Great! Keep practicing!"
console.log(`Strength: ${item.strength} → ${updated.strength}`);
```

## Testing

```bash
# Run all tests
python test_api.py

# SRS tests verify:
# - Initial strength = 0.2
# - Correct increases strength
# - Incorrect decreases strength
# - Bounds maintained [0.0, 1.0]
```
