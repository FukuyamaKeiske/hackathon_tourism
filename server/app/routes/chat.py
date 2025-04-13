from fastapi import APIRouter
from app.services.db import db_service
from app.schemas import ChatMessageResponse

from typing import List

router = APIRouter()


@router.get("/chat/{group_id}", response_model=List[ChatMessageResponse])
async def get_chat_messages(group_id: str):
    messages = await db_service.get_chat_messages(group_id=group_id)
    return [
        {
            "id": str(message["_id"]),
            "group_id": message["group_id"],
            "sender_id": message["sender_id"],
            "text": message["text"],
            "media_urls": message["media_urls"],
            "timestamp": message["timestamp"]
        }
        for message in messages
    ]
