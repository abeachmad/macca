# Quick Fix for Mic/Speaker Issues

## Problem
- HuggingFace API URL was wrong (`api-inference.huggingface.co` → deprecated)
- Getting 410 Gone errors
- Falling back to mock responses
- Mic/speaker not working

## Solution

**1. Stop services:**
```bash
./dev-stop.sh
```

**2. Backend .env is already fixed to:**
```
HF_API_BASE_URL=https://router.huggingface.co
```

**3. Restart services:**
```bash
./dev-start.sh
```

**4. Test mic:**
- Open http://localhost:3000
- Click mic button
- Allow microphone access
- Speak
- Should see real AI response (not mock)

## What Was Fixed

✅ Changed `HF_API_BASE_URL` from `api-inference.huggingface.co` to `router.huggingface.co`
✅ Frontend mic code is correct (uses MediaRecorder API)
✅ Frontend sends audio as FormData to `/api/session/turn/audio`
✅ Backend processes audio with real HuggingFace models

## Verify It's Working

After restart, you should see in logs:
```
API Base: https://router.huggingface.co  ← Should be router, not api-inference
```

And when you speak:
```
HTTP Request: POST https://router.huggingface.co/models/...  ← Should be 200 OK, not 410
```

## If Still Not Working

1. Check browser console for errors
2. Verify microphone permissions in browser
3. Check backend logs for 200 OK responses (not 410)
4. Try text input first to verify backend is working
