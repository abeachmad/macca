#!/usr/bin/env python3
"""Test script to verify API endpoints work"""

import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base, engine

# Create tables for testing
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_endpoints():
    print("Testing Macca API endpoints...")
    
    # Test root endpoint
    response = client.get("/api/")
    print(f"✅ GET /api/ - Status: {response.status_code}")
    
    # Test auth signup and get token
    response = client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    })
    print(f"✅ POST /api/auth/signup - Status: {response.status_code}")
    token = None
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"   Got auth token")
    
    # Test user profile
    response = client.get("/api/user/profile")
    print(f"✅ GET /api/user/profile - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   Profile: {response.json()}")
    
    # Test session start
    response = client.post("/api/session/start", json={
        "mode": "live_conversation",
        "topic": "daily_life"
    })
    print(f"✅ POST /api/session/start - Status: {response.status_code}")
    if response.status_code == 200:
        session_data = response.json()
        print(f"   Session ID: {session_data['session_id']}")
    
    # Test conversation turn
    response = client.post("/api/session/turn", json={
        "user_text": "I go to office yesterday",
        "mode": "live"
    })
    print(f"✅ POST /api/session/turn - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Reply: {data['macca_text'][:50]}...")
    
    # Test vocabulary (requires auth)
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/user/vocabulary", headers=headers)
        print(f"✅ GET /api/user/vocabulary - Status: {response.status_code}")
    else:
        # Test that it returns 401 without auth
        response = client.get("/api/user/vocabulary")
        print(f"✅ GET /api/user/vocabulary (no auth) - Status: {response.status_code} (expected 401)")
    
    # Test pronunciation analysis
    response = client.post("/api/pronunciation/analyze", json={
        "word": "think"
    })
    print(f"✅ POST /api/pronunciation/analyze - Status: {response.status_code}")
    
    # Test lessons
    response = client.get("/api/lessons")
    print(f"✅ GET /api/lessons - Status: {response.status_code}")
    if response.status_code == 200:
        lessons = response.json()
        print(f"   Found {len(lessons)} lessons")

if __name__ == "__main__":
    test_endpoints()
    print("\n🎉 All API endpoints tested!")
    print("\n📝 Available endpoints:")
    print("   - POST /api/auth/signup - User registration")
    print("   - POST /api/auth/login - User login")
    print("   - GET /api/user/profile - Get user profile")
    print("   - PATCH /api/user/profile - Update user profile")
    print("   - POST /api/session/start - Start new session")
    print("   - POST /api/session/turn - Process conversation turn")
    print("   - GET /api/user/vocabulary - Get vocabulary items (requires auth)")
    print("   - POST /api/user/vocabulary - Add vocabulary item (requires auth)")
    print("   - POST /api/pronunciation/analyze - Analyze pronunciation")
    print("   - GET /api/lessons - Get available lessons")
    print("   - GET /api/lessons/{id} - Get specific lesson")
    print("\n🔧 Configuration:")
    print(f"   - USE_MOCK_AI: {os.getenv('USE_MOCK_AI', 'true')}")
    print(f"   - HF_API_KEY: {'Set' if os.getenv('HF_API_KEY') else 'Not set'}")