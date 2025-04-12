from fastapi import HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.models import User
from app.services.db import db_service

SECRET_KEY = "hackathonvoronkatourism"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Исправление: добавьте явное указание алгоритма
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user_from_token(token: str):
    try:
        # Исправление: убедитесь что токен приходит в правильном формате
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],  # Убедитесь что алгоритм в списке
            options={"verify_signature": True},  # Явная проверка подписи
        )

        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Missing 'sub' claim")

        user = await db_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise HTTPException(
            status_code=401, detail=f"Could not validate credentials: {str(e)}"
        )
