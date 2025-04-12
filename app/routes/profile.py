from fastapi import APIRouter, HTTPException, Depends
from app.services.db import db_service
from app.auth import get_current_user_from_token
from app.dependencies import get_current_user
from app.schemas import UserUpdate

router = APIRouter()


@router.put("/interests", response_model=dict)
async def update_interests(
    user_data: UserUpdate,  # Данные из тела запроса
    current_user: dict = Depends(get_current_user)
):    
    await db_service.update_user_interests(
        email=current_user["email"],
        interests=user_data.interests
    )
    return {"message": "Interests updated successfully"}
