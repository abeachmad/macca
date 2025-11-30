# Environment Setup Guide

## Overview

Macca uses environment variables to configure backend and frontend for different environments (development, production).

## Backend Environment Variables

### Development Setup

```bash
cd backend
cp .env.example .env
# Edit .env with your local settings
```

**Key Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://localhost/macca` |
| `USE_MOCK_AI` | Use mock AI providers (no external API) | `true` |
| `HF_API_KEY` | Hugging Face API key (only if USE_MOCK_AI=false) | Empty |
| `HF_API_BASE_URL` | Hugging Face Router API URL | `https://router.huggingface.co` |
| `JWT_SECRET_KEY` | Secret for JWT token signing | Random string |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |
| `LOG_LEVEL` | Logging level | `INFO` |

### Production Setup

```bash
cd backend
cp .env.production.example .env.production
# Edit .env.production with production values
```

**CRITICAL for Production:**
- `USE_MOCK_AI=false` - Use real Hugging Face API
- `HF_API_KEY` - Must be set with valid API key
- `JWT_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `CORS_ORIGINS` - Restrict to your domain only
- `DATABASE_URL` - Use managed PostgreSQL (not localhost)
- `LOG_LEVEL=WARNING` - Reduce log verbosity

## Frontend Environment Variables

### Development Setup

```bash
cd frontend
cp .env.example .env
# Usually no changes needed for local dev
```

**Key Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_BACKEND_URL` | Backend API URL | Empty (uses proxy) |
| `VITE_ENABLE_VISUAL_EDITS` | Enable visual editing tools | `false` |

**Note:** When `VITE_BACKEND_URL` is empty, Vite proxy forwards `/api` to `http://localhost:8000`.

### Production Setup

```bash
cd frontend
cp .env.production.example .env.production
# Edit with production backend URL
```

**CRITICAL for Production:**
- `VITE_BACKEND_URL=https://api.yourdomain.com` - Full backend URL
- Build with: `npm run build` (automatically uses `.env.production`)

## Quick Start

### Local Development

```bash
# Backend
cd backend
cp .env.example .env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
cp .env.example .env
npm install
npm start
```

### Production Deployment

```bash
# Backend
cd backend
cp .env.production.example .env.production
# Edit .env.production with real values
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
cp .env.production.example .env.production
# Edit .env.production with backend URL
npm run build
# Serve build/ folder with nginx/caddy/etc
```

## Environment Variable Priority

**Backend:**
1. System environment variables (highest priority)
2. `.env` file
3. Default values in code

**Frontend (Vite):**
1. `.env.production` (when running `npm run build`)
2. `.env.development` (when running `npm start`)
3. `.env` (fallback)

## Security Best Practices

### DO NOT:
- ❌ Commit `.env` files to git (already in `.gitignore`)
- ❌ Use same `JWT_SECRET_KEY` in dev and prod
- ❌ Set `CORS_ORIGINS=*` in production
- ❌ Use `USE_MOCK_AI=true` in production
- ❌ Hardcode secrets in code

### DO:
- ✅ Use `.env.example` as template
- ✅ Generate strong random secrets for production
- ✅ Use environment variables in CI/CD (GitHub Secrets, etc.)
- ✅ Restrict CORS to your actual domain
- ✅ Use managed database services in production
- ✅ Rotate secrets periodically

## Troubleshooting

### Backend won't start
```bash
# Check if .env exists
ls backend/.env

# Check if all required vars are set
cat backend/.env

# Check logs
tail -f logs/backend.log
```

### Frontend can't connect to backend
```bash
# Check VITE_BACKEND_URL
cat frontend/.env

# Check if backend is running
curl http://localhost:8000/api/health/live

# Check browser console for CORS errors
```

### HuggingFace API errors
```bash
# Verify API key is set
echo $HF_API_KEY

# Test with mock mode first
USE_MOCK_AI=true uvicorn app.main:app --reload

# Check HF API status
curl -H "Authorization: Bearer $HF_API_KEY" \
  https://router.huggingface.co/models/SeaLLMs/SeaLLMs-v3-7B-Chat
```

## Example Production Deployment

### Using Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    env_file: ./backend/.env.production
    ports:
      - "8000:8000"
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: macca
      POSTGRES_USER: macca
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Using Nginx

```nginx
# /etc/nginx/sites-available/macca
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/macca/frontend/build;
        try_files $uri /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Generating Secrets

```bash
# JWT Secret (32 bytes hex)
openssl rand -hex 32

# Or use Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Or use Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```
