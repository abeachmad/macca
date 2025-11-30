# End-to-End Test Checklist

## Prerequisites
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database accessible (PostgreSQL or SQLite)

## Test Scenarios

### 1. Backend Health Check
```bash
curl http://localhost:8000/api/health/live
curl http://localhost:8000/api/health/ready
```
**Expected:** Both return `{"status": "ok"}`

### 2. User Profile (No Auth)
```bash
curl http://localhost:8000/api/user/profile
```
**Expected:** Returns mock user profile

### 3. Session Start
```bash
curl -X POST http://localhost:8000/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "live_conversation", "topic": "daily_life"}'
```
**Expected:** Returns session_id and initial_prompt

### 4. Conversation Turn
```bash
curl -X POST http://localhost:8000/api/session/turn \
  -H "Content-Type: application/json" \
  -d '{"user_text": "I go to office yesterday", "mode": "live"}'
```
**Expected:** Returns macca_text with feedback

### 5. Vocabulary List (No Auth)
```bash
curl http://localhost:8000/api/user/vocabulary
```
**Expected:** Returns empty array (backward compatible)

### 6. Auth Signup
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'
```
**Expected:** Returns access_token
**Save token for next tests**

### 7. Add Vocabulary (With Auth)
```bash
TOKEN="<your_token_here>"
curl -X POST http://localhost:8000/api/user/vocabulary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"word": "experience", "translation": "pengalaman", "example": "I have experience", "source": "test"}'
```
**Expected:** Returns vocabulary item with strength=0.2

### 8. Get Vocabulary for Review (SRS)
```bash
curl -X POST http://localhost:8000/api/user/vocabulary/review/next \
  -H "Authorization: Bearer $TOKEN"
```
**Expected:** Returns items array with the vocabulary we just added

### 9. Submit Review Answer (Correct)
```bash
VOCAB_ID="<id_from_previous_response>"
curl -X POST http://localhost:8000/api/user/vocabulary/review/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"vocabulary_id": "'$VOCAB_ID'", "correct": true}'
```
**Expected:** Returns updated item with strength=0.4

### 10. Submit Review Answer (Incorrect)
```bash
curl -X POST http://localhost:8000/api/user/vocabulary/review/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"vocabulary_id": "'$VOCAB_ID'", "correct": false}'
```
**Expected:** Returns updated item with strength~0.1

### 11. Pronunciation Analysis
```bash
curl -X POST http://localhost:8000/api/pronunciation/analyze \
  -H "Content-Type: application/json" \
  -d '{"word": "think"}'
```
**Expected:** Returns pronunciation feedback

### 12. Get Lessons
```bash
curl http://localhost:8000/api/lessons
```
**Expected:** Returns array of lessons

## Frontend Manual Tests

### 1. Home Page
- [ ] Open http://localhost:3000
- [ ] Page loads without errors
- [ ] No console errors

### 2. Live Conversation
- [ ] Click "Live Conversation"
- [ ] Type a message and send
- [ ] Verify response appears
- [ ] Check feedback panel shows

### 3. Pronunciation Coach
- [ ] Navigate to Pronunciation Coach
- [ ] Select a sound
- [ ] Practice a word
- [ ] Verify feedback appears

### 4. Profile
- [ ] Navigate to Profile
- [ ] Verify user info displays
- [ ] Try updating profile

### 5. Vocabulary
- [ ] Navigate to Vocabulary (if exists)
- [ ] Verify vocabulary list loads
- [ ] Try adding a word

## Test Results

Date: ___________
Tester: ___________

| Test | Status | Notes |
|------|--------|-------|
| Backend Health | ⬜ Pass ⬜ Fail | |
| User Profile | ⬜ Pass ⬜ Fail | |
| Session Start | ⬜ Pass ⬜ Fail | |
| Conversation Turn | ⬜ Pass ⬜ Fail | |
| Vocabulary List | ⬜ Pass ⬜ Fail | |
| Auth Signup | ⬜ Pass ⬜ Fail | |
| Add Vocabulary | ⬜ Pass ⬜ Fail | |
| SRS Review Next | ⬜ Pass ⬜ Fail | |
| SRS Answer Correct | ⬜ Pass ⬜ Fail | |
| SRS Answer Incorrect | ⬜ Pass ⬜ Fail | |
| Pronunciation | ⬜ Pass ⬜ Fail | |
| Get Lessons | ⬜ Pass ⬜ Fail | |
| Frontend Home | ⬜ Pass ⬜ Fail | |
| Frontend Conversation | ⬜ Pass ⬜ Fail | |
| Frontend Pronunciation | ⬜ Pass ⬜ Fail | |
| Frontend Profile | ⬜ Pass ⬜ Fail | |
| Frontend Vocabulary | ⬜ Pass ⬜ Fail | |

## Issues Found

1. 
2. 
3. 

## Overall Status
⬜ All tests passed - Ready for CI/CD
⬜ Some tests failed - Needs fixes
⬜ Major issues - Needs investigation
