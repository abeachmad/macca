# Development Scripts

Skrip untuk mempermudah development Macca.

## Setup Awal

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env sesuai kebutuhan
```

### Frontend
```bash
cd frontend
npm install --legacy-peer-deps
```

## Menjalankan Development Environment

### Start Backend + Frontend
```bash
./dev-start.sh
```

Skrip ini akan:
- ✅ Start backend di port 8000
- ✅ Start frontend di port 3000
- ✅ Simpan logs ke `logs/backend.log` dan `logs/frontend.log`
- ✅ Tampilkan backend log secara real-time
- ✅ Simpan PID untuk stop nanti

**URLs:**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

**Melihat Logs:**
```bash
# Backend log
tail -f logs/backend.log

# Frontend log
tail -f logs/frontend.log

# Keduanya sekaligus
tail -f logs/*.log
```

### Stop Semua Proses
```bash
./dev-stop.sh
```

Skrip ini akan:
- ✅ Stop backend dan frontend dari PID
- ✅ Kill semua proses di port 8000
- ✅ Kill semua proses di port 3000
- ✅ Kill proses uvicorn dan react-scripts yang masih jalan
- ✅ Bersihkan semua port

## Manual Commands

### Backend Only
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Frontend Only
```bash
cd frontend
npm start
```

### Check Ports
```bash
# Cek port 8000 (backend)
lsof -i:8000

# Cek port 3000 (frontend)
lsof -i:3000

# Kill manual
kill -9 $(lsof -ti:8000)
kill -9 $(lsof -ti:3000)
```

## Troubleshooting

### Port sudah digunakan
```bash
# Stop semua dulu
./dev-stop.sh

# Atau kill manual
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### Backend tidak start
```bash
# Cek log
cat logs/backend.log

# Cek venv
ls backend/venv/

# Re-install dependencies
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend tidak start
```bash
# Cek log
cat logs/frontend.log

# Cek node_modules
ls frontend/node_modules/

# Re-install dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Tips

### Background Development
Jika ingin menjalankan tanpa melihat log:
```bash
./dev-start.sh
# Tekan Ctrl+C setelah log muncul
# Proses tetap jalan di background
```

### Restart Backend Only
```bash
# Kill backend
lsof -ti:8000 | xargs kill -9

# Start ulang
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Restart Frontend Only
```bash
# Kill frontend
lsof -ti:3000 | xargs kill -9

# Start ulang
cd frontend
npm start
```
