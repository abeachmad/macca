"""
Vercel ASGI handler for FastAPI
"""
from app.main import app

# Vercel expects 'app' or 'application' variable
application = app
