from fastapi import APIRouter, Depends
from app.services.db import db_service
from app.auth import get_current_user_from_token
from app.schemas import GroupTourCreate, GroupTourResponse

from typing import List

router = APIRouter()


@router.post("/group-tours/create", response_model=GroupTourResponse)
async def create_group_tour(
    tour_data: GroupTourCreate,
    current_user: dict = Depends(get_current_user_from_token),
):
    coordinates = tour_data.coordinates
    tour = await db_service.create_group_tour(
        name=tour_data.name, description=tour_data.description, coordinates=coordinates
    )
    return {
        "id": str(tour["_id"]),
        "name": tour["name"],
        "description": tour["description"],
        "coordinates": tour["coordinates"],
        "participants": tour["participants"],
    }


@router.get("/group-tours/nearby", response_model=List[GroupTourResponse])
async def get_nearby_group_tours(lat: float, lng: float):
    tours = await db_service.db.group_tours.find(
        {
            "coordinates.lat": {"$gte": lat - 0.01, "$lte": lat + 0.01},
            "coordinates.lng": {"$gte": lng - 0.01, "$lte": lng + 0.01},
        }
    ).to_list(10)
    return [
        {
            "id": str(tour["_id"]),
            "name": tour["name"],
            "description": tour["description"],
            "coordinates": tour["coordinates"],
            "participants": tour["participants"],
        }
        for tour in tours
    ]
