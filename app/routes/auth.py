from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.services.db import db_service
from app.auth import create_access_token
from app.schemas import UserCreate, LoginResponse, UserLogin

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


@router.post("/register")
async def register_user(user_data: UserCreate):
    user = await db_service.get_user_by_email(user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = get_password_hash(user_data.password)
    await db_service.create_user(
        email=user_data.email,
        password_hash=password_hash,
        interests=user_data.interests,
    )
    return {"message": "User registered successfully"}


@router.post("/login", response_model=LoginResponse)
async def login_user(user: UserLogin):
    user_data = await db_service.get_user_by_email(user.email)
    if not user or not verify_password(user.password, user_data["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user_data["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
