from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.models import User, Place, GroupTour, ChatMessage


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
            "coordinates.lat": {"$gte": lat - 0.01, "$lte": lat + 0.01},
            "coordinates.lng": {"$gte": lng - 0.01, "$lte": lng + 0.01},
            "type": place_type,
        }
        return await self.db.places.find(query).to_list(10)

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


# Инициализация сервиса
db_service = DatabaseService(
    uri="mongodb://localhost:27017/",
    db_name="tourism_db",
)
