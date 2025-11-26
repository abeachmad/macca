#!/usr/bin/env python3
"""Test script to verify API endpoints work"""

import os
# Set test environment before importing anything else
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["USE_MOCK_AI"] = "true"
os.environ["HF_API_KEY"] = ""  # Ensure no HF key in tests

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
    import random
    test_email = f"test{random.randint(1000,9999)}@example.com"
    response = client.post("/api/auth/signup", json={
        "email": test_email,
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
    
    # Test vocabulary with auth
    vocab_id = None
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/user/vocabulary", headers=headers)
        print(f"✅ GET /api/user/vocabulary (with auth) - Status: {response.status_code}")
        
        # Add a vocabulary item for SRS testing
        response = client.post("/api/user/vocabulary", headers=headers, json={
            "word": "experience",
            "translation": "pengalaman",
            "example": "I have five years of experience.",
            "source": "test"
        })
        print(f"✅ POST /api/user/vocabulary (with auth) - Status: {response.status_code}")
        if response.status_code == 200:
            vocab_data = response.json()
            vocab_id = vocab_data["id"]
            assert vocab_data["strength"] == 0.2, "Initial strength should be 0.2"
            print(f"   Added vocab with initial strength: {vocab_data['strength']}")
    
    # Test vocabulary without auth (backward compatibility)
    response = client.get("/api/user/vocabulary")
    print(f"✅ GET /api/user/vocabulary (no auth) - Status: {response.status_code}")
    if response.status_code == 200:
        vocab_data = response.json()
        assert isinstance(vocab_data, list), "Vocabulary should return a list"
        print(f"   Returns list (backward compatible)")
    
    # Test health endpoints
    response = client.get("/api/health/live")
    print(f"✅ GET /api/health/live - Status: {response.status_code}")
    if response.status_code == 200:
        health_data = response.json()
        assert health_data["status"] == "ok", "Health status should be ok"
    
    response = client.get("/api/health/ready")
    print(f"✅ GET /api/health/ready - Status: {response.status_code}")
    if response.status_code == 200:
        ready_data = response.json()
        assert ready_data["database"] == "ok", "Database should be ok"
        print(f"   Database: {ready_data['database']}")
    
    # Test pronunciation analysis
    response = client.post("/api/pronunciation/analyze", json={
        "word": "think"
    })
    print(f"✅ POST /api/pronunciation/analyze - Status: {response.status_code}")
    
    # Test SRS endpoints
    if token and vocab_id:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test get items for review
        response = client.post("/api/user/vocabulary/review/next", headers=headers)
        print(f"✅ POST /api/user/vocabulary/review/next - Status: {response.status_code}")
        if response.status_code == 200:
            review_data = response.json()
            assert "items" in review_data, "Should return items array"
            print(f"   Got {len(review_data['items'])} items for review")
        
        # Test submit correct answer
        response = client.post("/api/user/vocabulary/review/answer", headers=headers, json={
            "vocabulary_id": vocab_id,
            "correct": True
        })
        print(f"✅ POST /api/user/vocabulary/review/answer (correct) - Status: {response.status_code}")
        if response.status_code == 200:
            answer_data = response.json()
            new_strength = answer_data["item"]["strength"]
            assert new_strength == 0.4, f"Strength should increase to 0.4, got {new_strength}"
            assert 0.0 <= new_strength <= 1.0, "Strength must be between 0 and 1"
            print(f"   Strength increased to: {new_strength}")
        
        # Test submit incorrect answer
        response = client.post("/api/user/vocabulary/review/answer", headers=headers, json={
            "vocabulary_id": vocab_id,
            "correct": False
        })
        print(f"✅ POST /api/user/vocabulary/review/answer (incorrect) - Status: {response.status_code}")
        if response.status_code == 200:
            answer_data = response.json()
            new_strength = answer_data["item"]["strength"]
            assert abs(new_strength - 0.1) < 0.01, f"Strength should decrease to ~0.1, got {new_strength}"
            assert 0.0 <= new_strength <= 1.0, "Strength must be between 0 and 1"
            print(f"   Strength decreased to: {new_strength:.2f}")
    
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
    print("   - GET /api/user/vocabulary - Get vocabulary items (auth optional)")
    print("   - POST /api/user/vocabulary - Add vocabulary item (auth optional)")
    print("   - POST /api/user/vocabulary/review/next - Get items for SRS review (auth required)")
    print("   - POST /api/user/vocabulary/review/answer - Submit review answer (auth required)")
    print("   - GET /api/health/live - Liveness probe")
    print("   - GET /api/health/ready - Readiness probe")
    print("   - POST /api/pronunciation/analyze - Analyze pronunciation")
    print("   - GET /api/lessons - Get available lessons")
    print("   - GET /api/lessons/{id} - Get specific lesson")
    print("\n🔧 Configuration:")
    print(f"   - USE_MOCK_AI: {os.getenv('USE_MOCK_AI', 'true')}")
    print(f"   - HF_API_KEY: {'Set' if os.getenv('HF_API_KEY') else 'Not set'}")