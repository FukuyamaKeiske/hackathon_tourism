from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from jose import JWTError

from app.auth import get_current_user_from_token
from app.services.db import db_service
from app.services.chat_service import ChatManager
from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.group_tours import router as group_tours_router
from app.routes.recommendations import router as recommendations_router

from contextlib import asynccontextmanager

app = FastAPI(
    title="Travel Recommendations API",
    description="API для рекомендаций по путешествиям",
    version="1.0.0",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_service.client.server_info()
    print("database connected")
    yield
    await db_service.client.close()
    print("database disconnected")


@app.middleware("http")
async def authenticate_user(request, call_next):
    if request.url.path.startswith("/auth") or request.url.path.startswith("/ws"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")
    
    try:
        user = await get_current_user_from_token(token)
        request.state.user = user
        return await call_next(request)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Подключение маршрутов
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(
    recommendations_router, prefix="/recommendations", tags=["Recommendations"]
)
app.include_router(group_tours_router, prefix="/group-tours", tags=["Group Tours"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

# Инициализация менеджера чата
chat_manager = ChatManager()


# WebSocket для чата
@app.websocket("/ws/chat/{group_id}")
async def websocket_chat_endpoint(websocket: WebSocket, group_id: str):
    await chat_manager.connect(websocket, group_id)
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            if message_type == "send_message":
                await chat_manager.send_message(
                    group_id,
                    data["sender_id"],
                    data["text"],
                    data.get("media_urls", []),
                )
            elif message_type == "delete_message":
                await chat_manager.delete_message(group_id, data["message_id"])
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket, group_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
