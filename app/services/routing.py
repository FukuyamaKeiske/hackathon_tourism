import aiohttp
from typing import List, Dict
from app.models import Place


class RoutingService:
    @staticmethod
    async def optimize_route(places: List[Dict], start_lat: float, start_lng: float):
        # Используем OSRM для оптимизации маршрута
        coordinates = ";".join(
            [f"{p['coordinates']['lng']},{p['coordinates']['lat']}" for p in places]
        )
        osrm_url = f"http://router.project-osrm.org/trip/v1/driving/{coordinates}?roundtrip=false&source=first"

        async with aiohttp.ClientSession() as session:
            async with session.get(osrm_url) as response:
                data = await response.json()
                optimized_order = data["trips"][0]["geometry"]["coordinates"]

                # Сортируем места по оптимальному порядку
                optimized_places = []
                for coord in optimized_order:
                    lng, lat = coord
                    for place in places:
                        if (
                            abs(place["coordinates"]["lat"] - lat) < 0.001
                            and abs(place["coordinates"]["lng"] - lng) < 0.001
                        ):
                            optimized_places.append(place)
                            break
                return optimized_places
