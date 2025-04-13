from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import User, Place, GroupTour, ChatMessage, Booking, Achievement, Quest


class DatabaseService:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def create_user(self, email: str, password_hash: str, interests: dict):
        user = User(email=email, password_hash=password_hash, interests=interests)
        await self.db.users.insert_one(user.dict(by_alias=True))

    async def get_user_by_email(self, email: str):
        return await self.db.users.find_one({"email": email})

    async def update_user_interests(self, email: str, interests: dict):
        await self.db.users.update_one(
            {"email": email}, {"$set": {"interests": interests}}
        )

    async def find_places_nearby(self, lat: float, lng: float, place_type: str):
        query = {
            "coordinates.lat": {"$gte": lat - 0.05, "$lte": lat + 0.05},
            "coordinates.lng": {"$gte": lng - 0.05, "$lte": lng + 0.05},
            "type": place_type,
        }
        places = await self.db.places.find(query).to_list(10)
        return [
            {
                "place_id": str(place["_id"]),
                "name": place.get("name", "Без названия"),
                "description": place.get("description", ""),
                "coordinates": place["coordinates"],
                "type": place["type"],
                "cuisine": place.get("cuisine", ""),
                "halal": place.get("halal", "no"),
                "access": place.get("access", "public"),
                "gallery": place.get("gallery", []),
                "partner": True,
                "work_time": place.get("work_time", "Круглосуточно")  # Используем work_time или "Круглосуточно"
            }
            for place in places
        ]

    async def create_group_tour(self, name: str, description: str, coordinates: dict):
        tour = GroupTour(
            name=name, description=description, coordinates=coordinates, participants=[]
        )
        await self.db.group_tours.insert_one(tour.model_dump(by_alias=True))

    async def add_participant_to_tour(self, group_id: str, user_id: str):
        await self.db.group_tours.update_one(
            {"_id": ObjectId(group_id)}, {"$push": {"participants": user_id}}
        )

    async def send_chat_message(self, message: ChatMessage):
        await self.db.chat_messages.insert_one(message.dict(by_alias=True))

    async def get_chat_messages(self, group_id: str):
        return await self.db.chat_messages.find({"group_id": group_id}).to_list(100)

    async def update_user_km(self, email: str, total_km: float):
        await self.db.users.update_one(
            {"email": email}, {"$set": {"total_km": total_km}}
        )

    async def update_user_points(self, email: str, delta: int):
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")
        new_points = user["profile_points"] + delta
        if new_points < 0:
            raise ValueError("Not enough points")
        new_rank = self.calculate_rank(new_points)
        await self.db.users.update_one(
            {"email": email},
            {"$set": {"profile_points": new_points, "tourist_rank": new_rank}},
        )

    def calculate_rank(self, points: int) -> int:
        rank = 1
        required_points = 100
        total_required = 0
        while total_required + required_points <= points:
            total_required += required_points
            rank += 1
            required_points *= 2
        return rank

    async def complete_achievement(self, email: str, achievement_id: str):
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")
        achievements = user.get("achievements", [])
        for ach in achievements:
            if str(ach["_id"]) == achievement_id and not ach["completed"]:
                ach["completed"] = True
                reward = ach["reward_points"]
                new_points = user["profile_points"] + reward
                new_rank = self.calculate_rank(new_points)
                await self.db.users.update_one(
                    {"email": email},
                    {
                        "$set": {
                            "achievements": achievements,
                            "profile_points": new_points,
                            "tourist_rank": new_rank,
                        }
                    },
                )
                return
        raise ValueError("Achievement not found or already completed")

    async def get_all_quests(self):
        return await self.db.quests.find().to_list(None)

    async def update_quest_progress(
        self, email: str, quest_id: str, completed_steps: int
    ):
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")
        quests = user.get("quests", [])
        quest = await self.db.quests.find_one({"_id": ObjectId(quest_id)})
        if not quest:
            raise ValueError("Quest not found")
        total_steps = quest["total_steps"]
        if completed_steps > total_steps:
            completed_steps = total_steps
        quest_found = False
        for uq in quests:
            if str(uq["quest_id"]) == quest_id:
                quest_found = True
                uq["completed_steps"] = completed_steps
                uq["progress"] = (
                    (completed_steps / total_steps) * 100 if total_steps > 0 else 0
                )
                if completed_steps == total_steps:
                    uq["completed"] = True
                    reward = quest["reward_points"]
                    new_points = user["profile_points"] + reward
                    new_rank = self.calculate_rank(new_points)
                    await self.db.users.update_one(
                        {"email": email},
                        {
                            "$set": {
                                "quests": quests,
                                "profile_points": new_points,
                                "tourist_rank": new_rank,
                            }
                        },
                    )
                else:
                    await self.db.users.update_one(
                        {"email": email}, {"$set": {"quests": quests}}
                    )
                return
        if not quest_found:
            new_uq = {
                "quest_id": ObjectId(quest_id),
                "completed": False,
                "progress": (
                    (completed_steps / total_steps) * 100 if total_steps > 0 else 0
                ),
                "completed_steps": completed_steps,
            }
            quests.append(new_uq)
            await self.db.users.update_one(
                {"email": email}, {"$set": {"quests": quests}}
            )

    async def sell_souvenir(self, email: str, souvenir_id: str):
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")
        souvenirs = user.get("souvenirs", [])
        for souv in souvenirs:
            if str(souv["_id"]) == souvenir_id:
                price = souv["price"]
                new_points = user["profile_points"] + price
                new_rank = self.calculate_rank(new_points)
                souvenirs.remove(souv)
                await self.db.users.update_one(
                    {"email": email},
                    {
                        "$set": {
                            "souvenirs": souvenirs,
                            "profile_points": new_points,
                            "tourist_rank": new_rank,
                        }
                    },
                )
                return
        raise ValueError("Souvenir not found")

    async def create_booking(self, email: str, booking: Booking):
        user = await self.db.users.find_one({"email": email})
        if not user:
            raise ValueError("User not found")
        bookings = user.get("bookings", [])
        booking_dict = booking.dict(by_alias=True)
        booking_dict["_id"] = ObjectId()
        bookings.append(booking_dict)
        await self.db.users.update_one(
            {"email": email}, {"$set": {"bookings": bookings}}
        )
        return booking_dict


db_service = DatabaseService(
    uri="mongodb://localhost:27017/",
    db_name="tourism_db",
)
