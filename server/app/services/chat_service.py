from bson import ObjectId
from typing import Dict, Set
from datetime import datetime
from fastapi import WebSocket
from app.models import ChatMessage
from app.services.db import db_service


class ChatManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, group_id: str):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = set()
        self.active_connections[group_id].add(websocket)

    def disconnect(self, websocket: WebSocket, group_id: str):
        if group_id in self.active_connections:
            self.active_connections[group_id].discard(websocket)
            if not self.active_connections[group_id]:
                del self.active_connections[group_id]

    async def send_message(
        self, group_id: str, sender_id: str, text: str, media_urls: list
    ):
        message = ChatMessage(
            group_id=group_id,
            sender_id=sender_id,
            text=text,
            media_urls=media_urls,
            timestamp=datetime.utcnow(),
        )
        await db_service.send_chat_message(message)
        await self.broadcast_message(group_id, message.dict())

    async def delete_message(self, group_id: str, message_id: str):
        await db_service.db.chat_messages.delete_one({"_id": ObjectId(message_id)})
        await self.broadcast_message(
            group_id, {"type": "delete", "message_id": message_id}
        )

    async def broadcast_message(self, group_id: str, message_data: dict):
        if group_id in self.active_connections:
            for connection in self.active_connections[group_id]:
                await connection.send_json(message_data)


# Инициализация сервиса
chat_manager = ChatManager()
