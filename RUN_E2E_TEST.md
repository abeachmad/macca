# How to Run E2E Tests

## Quick Start

```bash
# 1. Start backend and frontend
./dev-start.sh

# 2. Wait for services to start (about 5 seconds)
# Press Ctrl+C to exit log view (services keep running)

# 3. Run automated tests (in new terminal)
./test-e2e.sh

# 4. Stop services when done
./dev-stop.sh
```

## What Gets Tested

The automated script tests:
- ✅ Health endpoints
- ✅ User profile
- ✅ Session start & conversation
- ✅ Auth signup
- ✅ Vocabulary CRUD
- ✅ SRS review system
- ✅ Pronunciation analysis
- ✅ Lessons

## Expected Output

```
🧪 Macca E2E Test Suite
=======================

Checking if backend is running...
✓ Backend is running

1. Testing health endpoints...
✓ Liveness check
✓ Readiness check

2. Testing user profile (no auth)...
✓ Get profile

...

=======================
✓ All tests passed!

Backend is ready for CI/CD setup.
```

## If Tests Fail

1. Check logs:
   ```bash
   tail -f logs/backend.log
   ```

2. Check if services are running:
   ```bash
   lsof -i:8000  # Backend
   lsof -i:3000  # Frontend
   ```

3. Restart services:
   ```bash
   ./dev-stop.sh
   ./dev-start.sh
   ```

## Manual Testing

For manual frontend testing, open http://localhost:3000 and follow the checklist in `E2E_TEST_CHECKLIST.md`.
