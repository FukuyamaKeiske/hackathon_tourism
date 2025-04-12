from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    interests: Dict[str, List[str]]


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    interests: Dict[str, List[str]]


class PlaceResponse(BaseModel):
    id: str
    name: str
    description: str
    coordinates: Dict[str, float]
    type: str


class GroupTourCreate(BaseModel):
    name: str
    description: str
    coordinates: Dict[str, float]


class GroupTourResponse(BaseModel):
    id: str
    name: str
    description: str
    coordinates: Dict[str, float]
    participants: List[str]


class ChatMessageCreate(BaseModel):
    group_id: str
    sender_id: str
    text: str
    media_urls: List[str]


class ChatMessageResponse(BaseModel):
    id: str
    group_id: str
    sender_id: str
    text: str
    media_urls: List[str]
    timestamp: datetime


class WebSocketMessage(BaseModel):
    type: str  # "send_message" | "delete_message"
    sender_id: str = None
    text: str = None
    media_urls: List[str] = []
    message_id: str = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class RouteRecommendationResponse(BaseModel):
    route: List[PlaceResponse]
