# Test Recording - Localhost

## Status: ✅ Recording WORKS!

Dari console log Anda:
```
Recording started
Audio chunk received: 1 bytes
Audio chunk received: 2093 bytes
... (22 chunks total)
Recording stopped. Total chunks: 22
Audio blob created: 41051 bytes ✅
Sending audio blob: 41051 bytes, type: audio/webm ✅
```

**Recording sudah berhasil mendeteksi suara!** Audio blob 41KB sudah terbuat.

## Masalah Sekarang: CORS Error

```
Access to XMLHttpRequest at 'http://localhost:8000/api/session/turn/audio' 
from origin 'http://localhost:3001' has been blocked by CORS policy
```

## Solusi:

### 1. Start Backend dengan Script
```bash
cd backend
bash start.sh
```

### 2. Verify Backend Running
```bash
curl http://localhost:8000/
# Should return: {"status":"ok","message":"Macca API is running"}
```

### 3. Test Recording di Browser
1. Buka http://localhost:3001
2. Klik microphone button
3. Bicara 2-3 detik
4. Klik stop
5. Lihat console - seharusnya tidak ada CORS error lagi

## Expected Console Output (Success):
```
Recording started
Audio chunk received: ... (multiple chunks)
Recording stopped. Total chunks: X
Audio blob created: XXXXX bytes
Sending audio blob: XXXXX bytes, type: audio/webm
Response received: {macca_text: "...", feedback: {...}}
```

## Jika Masih Error:

### Check Backend CORS Config
```bash
cd backend
cat .env | grep CORS
# Should show: CORS_ORIGINS=*
```

### Restart Backend
```bash
pkill -f uvicorn
cd backend
bash start.sh
```

### Check Backend Logs
```bash
tail -f logs/backend.log
```

## Next Steps After CORS Fixed:

1. ✅ Recording works (DONE)
2. ⏳ Fix CORS (IN PROGRESS)
3. ⏳ Test full flow: Record → ASR → LLM → TTS → Response
4. ⏳ Deploy to production (push to GitHub → Vercel auto-deploy)
