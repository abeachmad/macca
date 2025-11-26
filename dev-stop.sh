#!/bin/bash
# Skrip untuk menghentikan backend dan frontend serta kill semua port

echo "🛑 Stopping Macca Development Environment..."

# Stop proses dari PID files
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "   Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null
    fi
    rm logs/backend.pid
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "   Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null
    fi
    rm logs/frontend.pid
fi

# Kill semua proses di port 8000 (backend)
echo "   Killing processes on port 8000..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Kill semua proses di port 3000 (frontend)
echo "   Killing processes on port 3000..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Kill proses uvicorn yang mungkin masih jalan
pkill -f "uvicorn app.main:app" 2>/dev/null || true

# Kill proses npm/node yang mungkin masih jalan
pkill -f "react-scripts start" 2>/dev/null || true

echo ""
echo "✅ All processes stopped and ports cleared!"
echo ""
echo "📋 Verify:"
echo "   lsof -i:8000  # Should be empty"
echo "   lsof -i:3000  # Should be empty"
