import aiohttp
import asyncio
from typing import List, Dict
from app.core.config import settings  # Для настройки таймаутов

class GeolocationService:
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"
    
    @staticmethod
    async def find_places_nearby(lat: float, lng: float, place_type: str) -> List[Dict]:
        # Преобразование типов мест в теги OSM
        osm_tags = {
            "достопримечательности": "tourism=attraction",
            "рестораны": "amenity=restaurant",
            "бары": "amenity=bar",
            "активный отдых": "leisure=sports_centre",
            "парки": "leisure=park",
            "конференции и офисы": "building=office"
        }
        
        # Формируем Overpass QL запрос
        query = f"""
        [out:json];
        node[
            {osm_tags.get(place_type, "amenity=restaurant")}
            ](
            around:1000,  # Радиус 1 км
            {lat},
            {lng}
            );
        out body;
        """
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    GeolocationService.OVERPASS_URL,
                    data=query,
                    timeout=settings.OVERPASS_TIMEOUT
                ) as response:
                    data = await response.json()
                    return [
                        {
                            "name": element.get("tags", {}).get("name", "Без названия"),
                            "description": element.get("tags", {}).get("description", ""),
                            "coordinates": {
                                "lat": element.get("lat"),
                                "lng": element.get("lon")
                            },
                            "type": place_type,
                            "cuisine": element.get("tags", {}).get("cuisine", ""),  # Для фильтрации еды
                            "halal": "yes" if "halal" in element.get("tags", {}) else "no"
                        }
                        for element in data.get("elements", [])
                        if "lat" in element and "lon" in element
                    ]
            except Exception as e:
                print(f"Overpass API error: {str(e)}")
                return []

    @staticmethod
    async def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        # Используем OSRM для расчёта пешеходных маршрутов
        osrm_url = f"http://router.project-osrm.org/route/v1/walking/{lng1},{lat1};{lng2},{lat2}?overview=false"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(osrm_url) as response:
                    data = await response.json()
                    return data['routes'][0]['distance'] / 1000  # В километрах
            except Exception:
                # Резервный расчёт по формуле Haversine
                from math import radians, sin, cos, sqrt, atan2
                R = 6371.0
                lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
                dlat = lat2 - lat1
                dlng = lng2 - lng1
                a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c

# Инициализация сервиса
geolocation_service = GeolocationService()