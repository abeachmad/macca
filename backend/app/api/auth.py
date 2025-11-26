from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings
import hashlib

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# Mock user store (replace with database later)
mock_users = {}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    if request.email in mock_users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(request.password)
    user = {
        "email": request.email,
        "name": request.name,
        "password_hash": hashed_password,
        "level": "B1",
        "goal": "daily_conversation",
        "explanation_language": "id"
    }
    mock_users[request.email] = user
    
    access_token = create_access_token(data={"sub": request.email})
    return AuthResponse(
        access_token=access_token,
        user={k: v for k, v in user.items() if k != "password_hash"}
    )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    user = mock_users.get(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": request.email})
    return AuthResponse(
        access_token=access_token,
        user={k: v for k, v in user.items() if k != "password_hash"}
    )