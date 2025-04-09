from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from models import User, get_db
import random
import string

# 🔐 Auth router
auth_router = APIRouter(tags=["Authentication"])

# 🔒 Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 📥 Input Schemas
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 📤 Output Schema
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Pydantic v2 syntax

# 🧠 Utility: Suggest available usernames
def suggest_username(base_username: str, db: Session):
    suggestion = base_username
    while db.query(User).filter_by(username=suggestion).first():
        suffix = ''.join(random.choices(string.digits, k=3))
        suggestion = f"{base_username}{suffix}"
    return suggestion

# 🚀 Signup Route
@auth_router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="🚫 Email already registered. Please use a different email."
        )

    if db.query(User).filter_by(username=data.username).first():
        suggested = suggest_username(data.username, db)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"🚫 Username taken. Try something like '{suggested}'"
        )

    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=pwd_context.hash(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # frontend can display “User registered successfully”

# 🔐 Login Route
@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="🚫 Invalid email or password"
        )

    return {
        "message": "✅ Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }
