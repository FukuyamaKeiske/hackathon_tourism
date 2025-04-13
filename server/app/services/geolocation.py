import aiohttp
from typing import List, Dict
from app.core.config import settings


class GeolocationService:
    DGIS_API_URL = "https://catalog.api.2gis.com/3.0/items"

    # Маппинг категорий dest на rubric_id 2GIS (примерные ID, уточните в документации 2GIS)
    DGIS_RUBRICS = {
        "Исторические места": "attraction.monument",
        "Сады и парки": "recreation.park",
        "Агротуризм": "agrotourism",  # Уточните категорию
        "Рестораны": "catering.restaurant",
        "Музеи": "culture.museum",
        "Театры": "culture.theatre",
        "Клубы": "catering.nightclub",
        "Достопримечательности": "attraction",
        "Здоровье": "healthcare.spa",
        "Спорт": "sport",
        "Музыка": "music",  # Уточните категорию
        "Активный отдых": "sport.outdoor",
    }

    # Совместимость мест с параметром "with"
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

    async def find_places_nearby(
        self, lat: float, lng: float, place_type: str, radius: int = 10000
    ) -> List[Dict]:
        """Поиск мест через 2GIS API."""
        params = {
            "point": f"{lng},{lat}",
            "radius": radius,
            "type": "branch,attraction",
            "q": self.DGIS_RUBRICS.get(place_type, "tourism"),
            "key": settings.DGIS_API_KEY,
            "fields": "items.point,items.name,items.description,items.rubrics,items.access,items.external_content",
            "locale": "ru_RU",
            "sort": "distance",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.DGIS_API_URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    return [
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
                        }
                        for item in items
                        if "point" in item
                    ]
            except Exception as e:
                print(f"2GIS API error: {str(e)}")
                return []

    async def find_food_places(
        self, lat: float, lng: float, food_prefs: List[str], radius: int = 5000
    ) -> List[Dict]:
        """Поиск мест для еды с учетом предпочтений."""
        params = {
            "point": f"{lng},{lat}",
            "radius": radius,
            "type": "branch",
            "q": "catering.restaurant,catering.cafe",
            "key": settings.DGIS_API_KEY,
            "fields": "items.point,items.name,items.description,items.rubrics,items.access,items.external_content",
            "locale": "ru_RU",
            "sort": "distance",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.DGIS_API_URL, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    items = data.get("result", {}).get("items", [])
                    print(items)
                    places = [
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
                        }
                        for item in items
                        if "point" in item
                    ]

                    # Фильтрация по предпочтениям еды
                    filtered = []
                    for place in places:
                        cuisine = place["cuisine"].lower()
                        # if "Халяль" in food_prefs and place["halal"] != "yes":
                        #     continue
                        # if (
                        #     "Вегетарианство" in food_prefs
                        #     and "vegetarian" not in cuisine
                        # ):
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
            except Exception as e:
                print(f"2GIS API error: {str(e)}")
                return []

    async def calculate_distance(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ) -> float:
        osrm_url = f"http://router.project-osrm.org/route/v1/walking/{lng1},{lat1};{lng2},{lat2}?overview=false"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(osrm_url) as response:
                    data = await response.json()
                    return data["routes"][0]["distance"] / 1000
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
