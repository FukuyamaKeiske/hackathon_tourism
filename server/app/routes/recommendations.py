from fastapi import APIRouter, HTTPException, Depends
from app.services.db import db_service
from app.services.geolocation import geolocation_service
from app.services.routing import routing_service
from app.dependencies import get_current_user
from app.schemas import RouteRecommendationResponse, PlaceResponse
from typing import List, Dict

router = APIRouter()


async def filter_by_with(places: List[Dict], with_prefs: List[str]) -> List[Dict]:
    filtered = []
    for place in places:
        place_type = place["type"]
        for with_pref in with_prefs:
            if place_type in geolocation_service.WITH_COMPATIBILITY.get(with_pref, []):
                filtered.append(place)
                break
    return filtered


@router.post("/route", response_model=RouteRecommendationResponse)
async def recommend_route(
    lat: float, lng: float, current_user: dict = Depends(get_current_user)
):
    user = await db_service.get_user_by_email(current_user["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    dest_prefs = user["interests"].get("dest", [])
    with_prefs = user["interests"].get("with", [])
    food_prefs = user["interests"].get("food", [])

    main_places = []
    for place_type in dest_prefs:
        places = await geolocation_service.find_places_nearby(lat, lng, place_type)
        main_places.extend(places)

    main_places = await filter_by_with(main_places, with_prefs)
    if not main_places:
        return {"route": []}

    food_places = await geolocation_service.find_food_places(lat, lng, food_prefs)

    optimized_main = await routing_service.optimize_route(main_places, lat, lng)

    route = []
    main_count = len(optimized_main)
    if main_count == 0:
        route.extend(food_places)
    else:
        for i, place in enumerate(optimized_main):
            route.append(place)
            if i == main_count // 3 and food_places:
                route.append(food_places.pop(0))
            if i == 2 * main_count // 3 and food_places:
                route.append(food_places.pop(0))
        route.extend(food_places)

    start_point = {
        "place_id": "",
        "name": "Начало маршрута",
        "description": "Ваше текущее местоположение",
        "coordinates": {"lat": lat, "lng": lng},
        "type": "start",
        "cuisine": "",
        "halal": "no",
        "gallery": [],
        "partner": False,
        "work_time": "Круглосуточно",
    }
    route = [start_point] + route

    response_route = [
        PlaceResponse(
            id=place.get("place_id", ""),
            name=place["name"],
            description=place["description"],
            coordinates=place["coordinates"],
            type=place["type"],
            cuisine=place.get("cuisine", ""),
            halal=place.get("halal", "no"),
            gallery=place.get("gallery", []),
            partner=place.get("partner", False),
            work_time=place.get("work_time", "Круглосуточно"),
        )
        for place in route
    ]

    return {"route": response_route}
