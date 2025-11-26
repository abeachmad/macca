#!/bin/bash
# Skrip untuk menjalankan backend dan frontend sekaligus

echo "🚀 Starting Macca Development Environment..."

# Cek apakah backend sudah setup
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Backend venv tidak ditemukan. Jalankan setup dulu:"
    echo "   cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Cek apakah frontend sudah setup
if [ ! -d "frontend/node_modules" ]; then
    echo "⚠️  Frontend node_modules tidak ditemukan. Jalankan setup dulu:"
    echo "   cd frontend && npm install --legacy-peer-deps"
    exit 1
fi

# Buat direktori untuk logs
mkdir -p logs

# Start backend di background
echo "📦 Starting backend..."
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..
echo "   Backend PID: $BACKEND_PID"

# Tunggu backend siap
echo "⏳ Waiting for backend to start..."
sleep 3

# Start frontend di background
echo "🎨 Starting frontend..."
cd frontend
nohup npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Macca Development Environment Started!"
echo ""
echo "📍 URLs:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Logs:"
echo "   Backend:  tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 Untuk stop: ./dev-stop.sh"
echo ""

# Tampilkan backend log
echo "📄 Backend Log (Ctrl+C untuk keluar dari log, proses tetap jalan):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -f logs/backend.log
