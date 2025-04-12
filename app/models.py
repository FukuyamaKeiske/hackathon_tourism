from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    password_hash: str
    interests: Dict[
        str, List[str]
    ]  # Пример: {"куда": ["достопримечательности"], "с кем": ["семья"]}

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Place(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    coordinates: Dict[str, float]
    type: str
    cuisine: str = ""  # Новая строка
    halal: str = ""    # Новая строка


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
