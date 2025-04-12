from fastapi import APIRouter, HTTPException, Depends
from app.services.db import db_service
from app.dependencies import get_current_user
from app.schemas import UserUpdate
from app.schemas import (
    ProfileResponse,
    UpdateKmRequest,
    UpdatePointsRequest,
    UpdateQuestProgressRequest,
    BookingCreate,
    QuestWithProgress,
    Achievement,
    NFT,
    Booking,
)

from typing import List
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=ProfileResponse)
async def get_profile(current_user: dict = Depends(get_current_user)):
    user = await db_service.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    travel_days = (datetime.utcnow() - user["created_at"]).days
    return {
        "email": user["email"],
        "interests": user["interests"],
        "profile_points": user["profile_points"],
        "tourist_rank": user["tourist_rank"],
        "total_km": user["total_km"],
        "travel_days": travel_days,
        "achievements": user["achievements"],
        "quests": user["quests"],
        "nfts": user["nfts"],
        "souvenirs": user["souvenirs"],
        "bookings": user["bookings"],
        "groups": user["groups"],
    }


@router.put("/km", response_model=dict)
async def update_km(
    request: UpdateKmRequest, current_user: dict = Depends(get_current_user)
):
    await db_service.update_user_km(current_user["email"], request.total_km)
    return {"message": "Kilometers updated successfully"}


@router.put("/points", response_model=dict)
async def update_points(
    request: UpdatePointsRequest, current_user: dict = Depends(get_current_user)
):
    try:
        await db_service.update_user_points(current_user["email"], request.delta)
        return {"message": "Points updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/achievements", response_model=List[Achievement])
async def get_achievements(current_user: dict = Depends(get_current_user)):
    user = await db_service.get_user_by_email(current_user["email"])
    return user["achievements"]


@router.post("/achievements/{achievement_id}/complete", response_model=dict)
async def complete_achievement(
    achievement_id: str, current_user: dict = Depends(get_current_user)
):
    try:
        await db_service.complete_achievement(current_user["email"], achievement_id)
        return {"message": "Achievement completed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/quests", response_model=List[QuestWithProgress])
async def get_quests(current_user: dict = Depends(get_current_user)):
    quests = await db_service.get_all_quests()
    user = await db_service.get_user_by_email(current_user["email"])
    user_quests = {str(uq["quest_id"]): uq for uq in user.get("quests", [])}
    result = []
    for quest in quests:
        uq = user_quests.get(
            str(quest["_id"]),
            {"completed": False, "progress": 0.0, "completed_steps": 0},
        )
        result.append(
            {
                "id": str(quest["_id"]),
                "location": quest["location"],
                "title": quest["title"],
                "description": quest["description"],
                "coordinates": quest["coordinates"],
                "link": quest.get("link"),
                "reward_points": quest["reward_points"],
                "total_steps": quest["total_steps"],
                "completed": uq["completed"],
                "progress": uq["progress"],
                "completed_steps": uq["completed_steps"],
            }
        )
    return result


@router.post("/quests/{quest_id}/progress", response_model=dict)
async def update_quest_progress(
    quest_id: str,
    request: UpdateQuestProgressRequest,
    current_user: dict = Depends(get_current_user),
):
    try:
        await db_service.update_quest_progress(
            current_user["email"], quest_id, request.completed_steps
        )
        return {"message": "Quest progress updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/nfts", response_model=List[NFT])
async def get_nfts(current_user: dict = Depends(get_current_user)):
    user = await db_service.get_user_by_email(current_user["email"])
    return user["nfts"]


@router.post("/souvenirs/{souvenir_id}/sell", response_model=dict)
async def sell_souvenir(
    souvenir_id: str, current_user: dict = Depends(get_current_user)
):
    try:
        await db_service.sell_souvenir(current_user["email"], souvenir_id)
        return {"message": "Souvenir sold successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bookings", response_model=Booking)
async def create_booking(
    booking: BookingCreate, current_user: dict = Depends(get_current_user)
):
    booking_dict = await db_service.create_booking(
        current_user["email"], Booking(**booking.dict())
    )
    return booking_dict


@router.get("/groups", response_model=List[str])
async def get_groups(current_user: dict = Depends(get_current_user)):
    user = await db_service.get_user_by_email(current_user["email"])
    return user["groups"]


@router.put("/interests", response_model=dict)
async def update_interests(
    user_data: UserUpdate,  # Данные из тела запроса
    current_user: dict = Depends(get_current_user),
):
    await db_service.update_user_interests(
        email=current_user["email"], interests=user_data.interests
    )
    return {"message": "Interests updated successfully"}
