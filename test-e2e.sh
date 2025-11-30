#!/bin/bash
# Automated E2E test script for Macca backend

BASE_URL="http://localhost:8000"
TOKEN=""

echo "🧪 Macca E2E Test Suite"
echo "======================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

pass() {
    echo -e "${GREEN}✓${NC} $1"
}

fail() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

# Test 1: Health Check
echo "1. Testing health endpoints..."
curl -s $BASE_URL/api/health/live | grep -q '"status":"ok"' && pass "Liveness check" || fail "Liveness check"
curl -s $BASE_URL/api/health/ready | grep -q '"database":"ok"' && pass "Readiness check" || fail "Readiness check"

# Test 2: User Profile (no auth)
echo ""
echo "2. Testing user profile (no auth)..."
curl -s $BASE_URL/api/user/profile | grep -q '"name"' && pass "Get profile" || fail "Get profile"

# Test 3: Session Start
echo ""
echo "3. Testing session start..."
SESSION_RESPONSE=$(curl -s -X POST $BASE_URL/api/session/start \
  -H "Content-Type: application/json" \
  -d '{"mode": "live_conversation", "topic": "daily_life"}')
echo "$SESSION_RESPONSE" | grep -q '"session_id"' && pass "Start session" || fail "Start session"

# Test 4: Conversation Turn
echo ""
echo "4. Testing conversation turn..."
curl -s -X POST $BASE_URL/api/session/turn \
  -H "Content-Type: application/json" \
  -d '{"user_text": "I go to office yesterday", "mode": "live"}' | grep -q '"macca_text"' && pass "Conversation turn" || fail "Conversation turn"

# Test 5: Vocabulary (no auth)
echo ""
echo "5. Testing vocabulary (no auth)..."
curl -s $BASE_URL/api/user/vocabulary | grep -q '\[\]' && pass "Get vocabulary" || fail "Get vocabulary"

# Test 6: Auth Signup
echo ""
echo "6. Testing auth signup..."
RANDOM_EMAIL="test$(date +%s)@example.com"
SIGNUP_RESPONSE=$(curl -s -X POST $BASE_URL/api/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$RANDOM_EMAIL\", \"password\": \"password123\", \"name\": \"Test User\"}")

if echo "$SIGNUP_RESPONSE" | grep -q '"access_token"'; then
    TOKEN=$(echo "$SIGNUP_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    pass "Signup (token: ${TOKEN:0:20}...)"
else
    fail "Signup"
fi

# Test 7: Add Vocabulary (with auth)
echo ""
echo "7. Testing add vocabulary (with auth)..."
VOCAB_RESPONSE=$(curl -s -X POST $BASE_URL/api/user/vocabulary \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"word": "experience", "translation": "pengalaman", "example": "I have experience", "source": "test"}')

if echo "$VOCAB_RESPONSE" | grep -q '"strength":0.2'; then
    VOCAB_ID=$(echo "$VOCAB_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    pass "Add vocabulary (id: $VOCAB_ID)"
else
    fail "Add vocabulary"
fi

# Test 8: SRS Review Next
echo ""
echo "8. Testing SRS review next..."
curl -s -X POST $BASE_URL/api/user/vocabulary/review/next \
  -H "Authorization: Bearer $TOKEN" | grep -q '"items"' && pass "Get review items" || fail "Get review items"

# Test 9: SRS Answer Correct
echo ""
echo "9. Testing SRS answer (correct)..."
curl -s -X POST $BASE_URL/api/user/vocabulary/review/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"vocabulary_id\": \"$VOCAB_ID\", \"correct\": true}" | grep -q '"strength":0.4' && pass "Submit correct answer" || fail "Submit correct answer"

# Test 10: SRS Answer Incorrect
echo ""
echo "10. Testing SRS answer (incorrect)..."
curl -s -X POST $BASE_URL/api/user/vocabulary/review/answer \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"vocabulary_id\": \"$VOCAB_ID\", \"correct\": false}" | grep -q '"strength":0.1' && pass "Submit incorrect answer" || fail "Submit incorrect answer"

# Test 11: Pronunciation
echo ""
echo "11. Testing pronunciation analysis..."
curl -s -X POST $BASE_URL/api/pronunciation/analyze \
  -H "Content-Type: application/json" \
  -d '{"word": "think"}' | grep -q '"word"' && pass "Pronunciation analysis" || fail "Pronunciation analysis"

# Test 12: Lessons
echo ""
echo "12. Testing lessons..."
curl -s $BASE_URL/api/lessons | grep -q '\[' && pass "Get lessons" || fail "Get lessons"

echo ""
echo "======================="
echo -e "${GREEN}✓ All tests passed!${NC}"
echo ""
echo "Backend is ready for CI/CD setup."
