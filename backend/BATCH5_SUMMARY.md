# Batch 5: Learning Engine Enhancements

## Overview

Batch 5 strengthens Macca's learning engine by:
1. Hardening LLM prompts with few-shot examples and mode-specific instructions
2. Implementing a simple Spaced Repetition System (SRS) for vocabulary
3. Making LLM behavior adapt to session modes (live_conversation, guided_lesson, pronunciation_coach)
4. Adding comprehensive tests for SRS functionality

All changes are **backward compatible** with existing frontend contracts.

---

## 1. LLM Prompt Hardening

### Changes Made

**File**: `app/providers/huggingface_llm.py`

Enhanced `_build_system_prompt()` with:

#### Mode-Specific Instructions
- **live_conversation**: "Be conversational and encouraging. Ask follow-up questions to keep the conversation flowing naturally."
- **guided_lesson**: "Focus on teaching specific grammar points: {target_grammar}. Provide structured drills that practice the target grammar. Use lesson_step {lesson_step} to guide progression."
- **pronunciation_coach**: "Focus primarily on pronunciation feedback. Use 'repeat_sentence' drills to help the learner practice specific sounds."

#### Enhanced Context
Now includes in prompt:
- User's common_issues list
- Session's lesson_id, target_grammar, target_vocabulary, lesson_step
- Clear instructions to ALWAYS populate next_prompt and drills

#### Few-Shot Examples
Added 3 complete examples showing:
1. **Live conversation with grammar issue**: Past tense correction with drill
2. **Guided lesson**: Past simple teaching with structured drill
3. **Pronunciation coach**: TH sound practice with repeat drill

### Benefits
- More consistent JSON output from LLM
- Better structured feedback and drills
- Mode-appropriate responses
- Clearer examples for the model to follow

---

## 2. Simple Spaced Repetition System (SRS)

### New Service

**File**: `app/services/srs.py`

Implements simple strength-based SRS algorithm:

```python
# Constants
INITIAL_STRENGTH = 0.2      # New items start here
CORRECT_BOOST = 0.2         # Increase on correct answer
INCORRECT_PENALTY = 0.3     # Decrease on incorrect answer
MIN_STRENGTH = 0.0          # Floor
MAX_STRENGTH = 1.0          # Ceiling
```

#### Functions

**`get_items_for_review(user_id, db, limit=5)`**
- Returns vocabulary items prioritized by:
  1. Lowest strength first (items needing practice)
  2. Longest time since last review
- Default limit: 5 items

**`update_review_result(vocabulary_id, correct, db)`**
- Updates item strength based on answer:
  - Correct: `strength = min(1.0, strength + 0.2)`
  - Incorrect: `strength = max(0.0, strength - 0.3)`
- Updates `last_reviewed_at` timestamp
- Returns updated item

### New API Endpoints

**File**: `app/api/vocabulary.py`

#### POST `/api/user/vocabulary/review/next`
**Auth**: Required (returns 401 without valid token)

**Query Parameters**:
- `limit` (optional, default=5): Number of items to return

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

#### POST `/api/user/vocabulary/review/answer`
**Auth**: Required (returns 401 without valid token)

**Request Body**:
```json
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
    "translation": "pengalaman",
    "example": "I have five years of experience.",
    "source": "conversation",
    "strength": 0.4,
    "last_reviewed_at": "2024-01-15T11:00:00Z"
  },
  "message": "Great! Keep practicing."
}
```

**Error Responses**:
- 401: No valid auth token
- 403: User doesn't own this vocabulary item
- 404: Vocabulary item not found

### Database Changes

**File**: `app/db/models.py`

No schema changes needed. Existing `VocabularyItem` model already has:
- `strength` (Float, default=0.0)
- `last_reviewed_at` (DateTime, nullable)

### Updated Existing Endpoints

**POST `/api/user/vocabulary`**
- Now sets initial strength to `0.2` (INITIAL_STRENGTH constant)
- Previously defaulted to `0.0`

**GET `/api/user/vocabulary`**
- Now includes `last_reviewed_at` in response
- Backward compatible (field is nullable)

---

## 3. Mode-Aware LLM Behavior

### Implementation

The LLM prompt now branches based on `SessionContext.mode`:

**live_conversation**:
- Open-ended, conversational
- Encourages follow-up questions
- Natural flow

**guided_lesson**:
- Strongly guided by target_grammar
- Uses lesson_step for progression
- Structured drills matching learning objectives

**pronunciation_coach**:
- Focus on pronunciation feedback
- Short repeat_sentence drills
- Specific sound targeting

### No Breaking Changes

- `MaccaJsonResponse` schema unchanged
- `/api/session/turn` response shape unchanged
- Only internal prompt content adjusted

---

## 4. Tests

### Updated Test File

**File**: `test_api.py`

Added comprehensive SRS tests:

1. **Add vocabulary with auth**: Verifies initial strength = 0.2
2. **Get items for review**: Tests `/review/next` endpoint
3. **Submit correct answer**: Verifies strength increases (0.2 → 0.4)
4. **Submit incorrect answer**: Verifies strength decreases (0.4 → 0.1)
5. **Strength bounds**: Ensures 0.0 ≤ strength ≤ 1.0

### Test Results

All tests pass with `USE_MOCK_AI=true`:
```
✅ POST /api/user/vocabulary (with auth) - Status: 200
   Added vocab with initial strength: 0.2
✅ POST /api/user/vocabulary/review/next - Status: 200
   Got 1 items for review
✅ POST /api/user/vocabulary/review/answer (correct) - Status: 200
   Strength increased to: 0.4
✅ POST /api/user/vocabulary/review/answer (incorrect) - Status: 200
   Strength decreased to: 0.10
```

### Other Tests

- `test_llm_parsing.py`: ✅ All pass
- `test_provider_selection.py`: ✅ All pass

---

## Usage Examples

### Frontend Integration: SRS Review Flow

```typescript
// 1. Get items for review
const reviewResponse = await fetch('/api/user/vocabulary/review/next?limit=5', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` }
});
const { items } = await reviewResponse.json();

// 2. Show flashcard to user
const item = items[0];
console.log(`Word: ${item.word}`);
console.log(`Translation: ${item.translation}`);
console.log(`Example: ${item.example}`);
console.log(`Current strength: ${item.strength}`);

// 3. User answers (correct/incorrect)
const answerResponse = await fetch('/api/user/vocabulary/review/answer', {
  method: 'POST',
  headers: { 
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    vocabulary_id: item.id,
    correct: true  // or false
  })
});
const { item: updatedItem, message } = await answerResponse.json();
console.log(message); // "Great! Keep practicing!"
console.log(`New strength: ${updatedItem.strength}`);
```

### Backend: Using SRS Service

```python
from app.services import srs
from app.db.database import get_db

# Get items for review
items = srs.get_items_for_review(user_id="user_123", db=db, limit=5)

# Update after review
updated_item = srs.update_review_result(
    vocabulary_id="vocab_123",
    correct=True,
    db=db
)
print(f"New strength: {updated_item.strength}")
```

---

## SRS Algorithm Details

### Strength Progression Examples

**Starting from 0.2 (new item)**:
- Correct → 0.4
- Correct → 0.6
- Correct → 0.8
- Correct → 1.0 (mastered)

**From 0.6 (intermediate)**:
- Incorrect → 0.3
- Incorrect → 0.0 (needs review)

**From 1.0 (mastered)**:
- Incorrect → 0.7 (still strong but needs practice)

### Review Priority

Items are selected in this order:
1. Lowest strength (0.0 before 0.2 before 0.4, etc.)
2. Oldest last_reviewed_at (never reviewed first)
3. Limited to requested count (default 5)

### Future Enhancements (Not Implemented)

Potential improvements for future batches:
- Time-based intervals (review after 1 day, 3 days, 7 days, etc.)
- Difficulty levels per item
- Review history tracking
- Adaptive difficulty based on user level
- Leitner box system
- SM-2 or SM-18 algorithms

---

## Files Modified

### New Files
- `app/services/srs.py` - SRS algorithm implementation

### Modified Files
- `app/providers/huggingface_llm.py` - Enhanced prompt with few-shot examples and mode-specific instructions
- `app/api/vocabulary.py` - Added SRS endpoints, updated existing endpoints
- `test_api.py` - Added SRS tests

### Unchanged (Verified Compatible)
- `app/schemas/macca.py` - No schema changes
- `app/db/models.py` - No schema changes (fields already existed)
- `app/api/session.py` - No changes (uses enhanced LLM provider transparently)
- Frontend contracts - All backward compatible

---

## Configuration

No new environment variables required.

Existing configuration works as-is:
- `USE_MOCK_AI=true` - SRS works in mock mode
- `USE_MOCK_AI=false` - SRS works with real HuggingFace LLM

---

## Migration Notes

### For Existing Users

No database migration needed. Existing vocabulary items:
- Will have `strength=0.0` (can be reviewed immediately)
- Will have `last_reviewed_at=NULL` (prioritized for review)
- Will update to proper SRS values after first review

### For Frontend Developers

**New endpoints available**:
- `POST /api/user/vocabulary/review/next` - Get items for review
- `POST /api/user/vocabulary/review/answer` - Submit review result

**Updated response fields**:
- `GET /api/user/vocabulary` now includes `last_reviewed_at`
- `POST /api/user/vocabulary` now returns `last_reviewed_at`

**Auth requirement**:
- SRS endpoints require authentication (401 without token)
- Existing vocabulary endpoints remain backward compatible

---

## Testing Checklist

- ✅ All existing tests pass
- ✅ SRS endpoints return correct data
- ✅ Strength increases on correct answer
- ✅ Strength decreases on incorrect answer
- ✅ Strength stays within bounds [0.0, 1.0]
- ✅ Initial strength set to 0.2 for new items
- ✅ Review priority works (lowest strength first)
- ✅ Auth required for SRS endpoints
- ✅ No network calls in test mode
- ✅ LLM prompt includes mode-specific instructions
- ✅ Few-shot examples in prompt

---

## Summary

Batch 5 successfully strengthens Macca's learning engine with:

1. **Smarter LLM prompts**: Few-shot examples and mode-specific instructions produce more consistent, relevant feedback
2. **Working SRS system**: Simple but effective spaced repetition for vocabulary learning
3. **Mode-aware behavior**: LLM adapts to live_conversation, guided_lesson, and pronunciation_coach modes
4. **Full test coverage**: All new functionality tested with zero network calls

All changes maintain backward compatibility with existing frontend code.
