from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Optional
from .models import Achievement, UserQuest, NFT, DigitalSouvenir, Booking


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
    cuisine: Optional[str] = ""
    halal: Optional[str] = "no"
    gallery: List[str] = []
    partner: bool = False
    work_time: str = "Круглосуточно"


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


class ProfileResponse(BaseModel):
    email: str
    interests: Dict[str, List[str]]
    profile_points: int
    tourist_rank: int
    total_km: float
    travel_days: int
    achievements: List[Achievement]
    quests: List[UserQuest]
    nfts: List[NFT]
    souvenirs: List[DigitalSouvenir]
    bookings: List[Booking]
    groups: List[str]


class UpdateKmRequest(BaseModel):
    total_km: float


class UpdatePointsRequest(BaseModel):
    delta: int


class UpdateQuestProgressRequest(BaseModel):
    completed_steps: int


class BookingCreate(BaseModel):
    type: str
    details: Dict[str, str]


class QuestWithProgress(BaseModel):
    id: str
    location: str
    title: str
    description: str
    coordinates: Dict[str, float]
    link: Optional[str]
    reward_points: int
    total_steps: int
    completed: bool
    progress: float
    completed_steps: int
