from fastapi import APIRouter, HTTPException, Depends
from app.services.db import db_service
from app.services.geolocation import geolocation_service
from app.services.routing import RoutingService
from app.auth import get_current_user_from_token
from app.dependencies import get_current_user
from app.schemas import RouteRecommendationResponse, PlaceResponse

router = APIRouter()


@router.post("/route", response_model=RouteRecommendationResponse)
async def recommend_route(
    lat: float, lng: float, current_user: dict = Depends(get_current_user)
):
    user = await db_service.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    food_preferences = user["interests"].get("еда", [])
    optimized_places = []

    # Поиск мест по категориям
    for place_type in user["interests"].get("куда", []):
        nearby_places = await geolocation_service.find_places_nearby(
            lat, lng, place_type
        )

        # Фильтрация по еде
        filtered_places = []
        for place in nearby_places:
            if "халяль" in food_preferences and place["halal"] != "yes":
                continue
            if (
                "русская кухня" in food_preferences
                and "russian" not in place.get("cuisine", "").lower()
            ):
                continue
            filtered_places.append(place)

        optimized_places.extend(filtered_places)

    # Оптимизация маршрута
    routing_service = RoutingService()
    optimized_places = await routing_service.optimize_route(optimized_places, lat, lng)

    # Преобразование в схемы ответа
    route = []
    for place in optimized_places:
        route.append(
            PlaceResponse(
                id=place.get("place_id", ""),
                name=place["name"],
                description=place["description"],
                coordinates=place["coordinates"],
                type=place["type"],
            )
        )

    return {"route": route}
