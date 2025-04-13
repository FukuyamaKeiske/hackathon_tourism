import aiohttp
from typing import List, Dict
from app.core.config import settings


class RoutingService:
    DGIS_MATRIX_URL = "https://catalog.api.2gis.com/matrix"

    async def optimize_route(
        self, places: List[Dict], start_lat: float, start_lng: float
    ) -> List[Dict]:
        """Оптимизация маршрута с использованием 2GIS Distance Matrix API."""
        if not places:
            return []

        # Формируем список точек: старт + места
        points = [{"lon": start_lng, "lat": start_lat}] + [
            {"lon": p["coordinates"]["lng"], "lat": p["coordinates"]["lat"]}
            for p in places
        ]
        sources = [0]  # Стартовая точка
        targets = list(range(1, len(points)))  # Остальные точки

        # Запрос к 2GIS Distance Matrix
        payload = {
            "points": points,
            "sources": sources,
            "targets": targets,
            "transport": "walking",
            "type": "shortest",  # Минимизируем расстояние
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
                    response.raise_for_status()
                    data = await response.json()
                    distances = data.get("matrix", [])

                    if not distances:
                        return places  # Возвращаем без оптимизации, если данных нет

                    # Извлекаем расстояния от стартовой точки
                    distance_map = {}
                    for entry in distances[0]["targets"]:
                        target_index = entry["target_index"]
                        distance = (
                            entry.get("distance", {}).get("value", float("inf")) / 1000
                        )  # В километрах
                        distance_map[target_index - 1] = distance

                    # Сортируем места по расстоянию
                    optimized_indices = sorted(
                        range(len(places)),
                        key=lambda i: distance_map.get(i, float("inf")),
                    )
                    optimized_places = [places[i] for i in optimized_indices]
                    return optimized_places
            except Exception as e:
                print(f"2GIS Matrix API error: {str(e)}")
                return places  # Возвращаем исходный порядок в случае ошибки


routing_service = RoutingService()
