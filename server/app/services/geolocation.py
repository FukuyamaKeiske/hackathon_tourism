import aiohttp
from typing import List, Dict
from app.core.config import settings
from app.services.db import db_service
from datetime import datetime


class GeolocationService:
    DGIS_API_URL = "https://catalog.api.2gis.com/3.0/items"
    DGIS_MATRIX_URL = "https://catalog.api.2gis.com/matrix"

    DGIS_RUBRICS = {
        "Исторические места": "attraction.monument",
        "Сады и парки": "recreation.park",
        "Агротуризм": "agrotourism",
        "Рестораны": "catering.restaurant",
        "Музеи": "culture.museum",
        "Театры": "culture.theatre",
        "Клубы": "catering.nightclub",
        "Достопримечательности": "attraction",
        "Здоровье": "healthcare.spa",
        "Спорт": "sport",
        "Музыка": "music",
        "Активный отдых": "sport.outdoor",
    }

    WITH_COMPATIBILITY = {
        "Один": [
            "Клубы",
            "Здоровье",
            "Спорт",
            "Активный отдых",
            "Музеи",
            "Агротуризм",
            "Музыка",
            "Рестораны",
            "Театры",
            "Достопримечательности",
            "Сады и парки",
            "Исторические места",
        ],
        "Семья": [
            "Клубы",
            "Здоровье",
            "Спорт",
            "Активный отдых",
            "Музеи",
            "Агротуризм",
            "Музыка",
            "Рестораны",
            "Театры",
            "Достопримечательности",
            "Сады и парки",
            "Исторические места",
        ],
        "Бизнес": [
            "Клубы",
            "Здоровье",
            "Спорт",
            "Активный отдых",
            "Музеи",
            "Агротуризм",
            "Музыка",
            "Рестораны",
            "Театры",
            "Достопримечательности",
            "Сады и парки",
            "Исторические места",
        ],
    }

    def _parse_schedule(self, schedule: Dict) -> str:
        """Извлечение времени работы для текущего дня (Понедельник)."""
        if not schedule:
            return "Круглосуточно"

        # Предполагаем, что текущий день — Понедельник
        current_day = "Mon"
        days = schedule.keys()

        for day in days:
            if day == current_day:
                working_hours = schedule[day].get("working_hours", [])
                if working_hours:
                    # Берем первый интервал времени
                    time_from = working_hours[0].get("from", "")
                    time_to = working_hours[0].get("to", "")
                    if time_from and time_to:
                        return f"{time_from[:5]}-{time_to[:5]}"  # Формат ЧЧ:ММ-ЧЧ:ММ
                break

        return "Круглосуточно"

    async def find_places_nearby(
        self, lat: float, lng: float, place_type: str, radius: int = 7000
    ) -> List[Dict]:
        # Поиск партнерских мест из базы
        partner_places = await db_service.find_places_nearby(lat, lng, place_type)

        # Поиск мест через 2GIS API
        params = {
            "point": f"{lng},{lat}",
            "radius": radius,
            "type": "branch,attraction",
            "q": self.DGIS_RUBRICS.get(place_type, "tourism"),
            "key": settings.DGIS_API_KEY,
            "fields": "items.point,items.name,items.description,items.rubrics,items.access,items.external_content,items.schedule",
            "locale": "ru_RU",
            "sort": "distance",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.DGIS_API_URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    dgis_places = [
                        {
                            "place_id": item["id"],
                            "name": item.get("name", "Без названия"),
                            "description": item.get("description", ""),
                            "coordinates": {
                                "lat": item["point"]["lat"],
                                "lng": item["point"]["lon"],
                            },
                            "type": place_type,
                            "cuisine": ",".join(
                                [
                                    rubric.get("name", "")
                                    for rubric in item.get("rubrics", [])
                                    if "catering" in rubric.get("kind", "")
                                ]
                            ),
                            "halal": (
                                "yes"
                                if any(
                                    "halal" in rubric.get("name", "").lower()
                                    for rubric in item.get("rubrics", [])
                                )
                                else "no"
                            ),
                            "access": item.get("access", "public"),
                            "gallery": [
                                content["main_photo_url"]
                                for content in item.get("external_content", [])
                                if content.get("type") in ["photo", "photo_album"]
                                and "main_photo_url" in content
                            ],
                            "partner": False,
                            "work_time": self._parse_schedule(item.get("schedule", {})),
                        }
                        for item in items
                        if "point" in item
                    ]
            except Exception as e:
                print(f"2GIS API error: {str(e)}")
                dgis_places = []

        return partner_places + dgis_places

    async def find_food_places(
        self, lat: float, lng: float, food_prefs: List[str], radius: int = 5000
    ) -> List[Dict]:
        # Поиск партнерских мест для еды
        partner_places = await db_service.find_places_nearby(lat, lng, "restaurant")

        # Поиск мест через 2GIS API
        params = {
            "point": f"{lng},{lat}",
            "radius": radius,
            "type": "branch",
            "q": "catering.restaurant,catering.cafe",
            "key": settings.DGIS_API_KEY,
            "fields": "items.point,items.name,items.description,items.rubrics,items.access,items.external_content,items.schedule",
            "locale": "ru_RU",
            "sort": "distance",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.DGIS_API_URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    dgis_places = [
                        {
                            "place_id": item["id"],
                            "name": item.get("name", "Без названия"),
                            "description": item.get("description", ""),
                            "coordinates": {
                                "lat": item["point"]["lat"],
                                "lng": item["point"]["lon"],
                            },
                            "type": "restaurant",
                            "cuisine": ",".join(
                                [
                                    rubric.get("name", "")
                                    for rubric in item.get("rubrics", [])
                                    if "catering" in rubric.get("kind", "")
                                ]
                            ),
                            "halal": (
                                "yes"
                                if any(
                                    "halal" in rubric.get("name", "").lower()
                                    for rubric in item.get("rubrics", [])
                                )
                                else "no"
                            ),
                            "access": item.get("access", "public"),
                            "gallery": [
                                content["main_photo_url"]
                                for content in item.get("external_content", [])
                                if content.get("type") == "photo"
                                and "main_photo_url" in content
                            ],
                            "partner": False,
                            "work_time": self._parse_schedule(item.get("schedule", {})),
                        }
                        for item in items
                        if "point" in item
                    ]
            except Exception as e:
                print(f"2GIS API error: {str(e)}")
                dgis_places = []

        places = partner_places + dgis_places

        filtered = []
        for place in places:
            cuisine = place["cuisine"].lower()
            # if "Халяль" in food_prefs and place["halal"] != "yes":
            #     continue
            # if "Вегетарианство" in food_prefs and "vegetarian" not in cuisine:
            #     continue
            # if "Мясо птицы" in food_prefs and "chicken" not in cuisine:
            #     continue
            # if "Мясо животных" in food_prefs and "meat" not in cuisine:
            #     continue
            # if "Морепродукты" in food_prefs and "seafood" not in cuisine:
            #     continue
            # if "Десерты" in food_prefs and "dessert" not in cuisine:
            #     continue
            filtered.append(place)
        return filtered[:4]

    async def calculate_distance(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ) -> float:
        payload = {
            "points": [{"lon": lng1, "lat": lat1}, {"lon": lng2, "lat": lat2}],
            "sources": [0],
            "targets": [1],
            "transport": "walking",
            "type": "shortest",
        }
        params = {
            "key": settings.DGIS_API_KEY,
            "version": "2.0",
            "response_format": "json",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.DGIS_MATRIX_URL, json=payload, params=params
                ) as response:
                    data = await response.json()
                    distance = (
                        data["matrix"][0]["targets"][0]["distance"]["value"] / 1000
                    )
                    return distance
            except Exception:
                from math import radians, sin, cos, sqrt, atan2

                R = 6371.0
                lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
                dlat = lat2 - lat1
                dlng = lng2 - lng1
                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c


geolocation_service = GeolocationService()
