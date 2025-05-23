from bson import ObjectId
from datetime import datetime
from pydantic_core import core_schema
from typing import List, Dict, Optional, Any
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: Any, info: Any = None) -> ObjectId:
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str) and ObjectId.is_valid(value):
                return ObjectId(value)
            raise ValueError("Invalid ObjectId")

        return core_schema.with_info_plain_validator_function(
            validate,
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> dict[str, Any]:
        return handler(core_schema.str_schema())


class Achievement(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    icon: str
    description: str
    reward_points: int
    completed: bool = False
    nft_id: Optional[PyObjectId] = None
    souvenir_id: Optional[PyObjectId] = None


class UserQuest(BaseModel):
    quest_id: PyObjectId
    completed: bool = False
    progress: float = 0.0
    completed_steps: int = 0


class NFT(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    from_achievement: bool
    description: str
    image: str
    buy_price: Optional[float] = None
    sell_price: Optional[float] = None


class DigitalSouvenir(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    icon: str
    description: str
    price: int


class Booking(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    type: str
    details: Dict[str, str]


class Quest(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    location: str
    title: str
    description: str
    coordinates: Dict[str, float]
    link: Optional[str] = None
    reward_points: int
    total_steps: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password_hash: str
    interests: Dict[str, List[str]]
    profile_points: int = 0
    tourist_rank: int = 0
    total_km: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    achievements: List[Achievement] = []
    quests: List[UserQuest] = []
    nfts: List[NFT] = []
    souvenirs: List[DigitalSouvenir] = []
    bookings: List[Booking] = []
    groups: List[str] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Place(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    coordinates: Dict[str, float]
    type: str
    cuisine: str = ""  # Новая строка
    halal: str = ""  # Новая строка


class GroupTour(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    coordinates: Dict[str, float]
    participants: List[str]  # Список ID пользователей


class ChatMessage(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    group_id: str
    sender_id: str
    text: str
    media_urls: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
