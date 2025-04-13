import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Request,
    APIRouter,
)
from fastapi.responses import HTMLResponse, JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from jose import JWTError
from app.auth import get_current_user_from_token
from app.services.db import db_service
from app.services.chat_service import ChatManager
from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.interests import router as interests_router
from app.routes.group_tours import router as group_tours_router
from app.routes.recommendations import router as recommendations_router
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Travel Recommendations API",
    description="API для рекомендаций по путешествиям",
    version="1.6.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_service.client.server_info()
    print("database connected")
    yield
    await db_service.client.close()
    print("database disconnected")


@app.middleware("http")
async def authenticate_user(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    # Пропускаем админ-панель без авторизации
    if request.url.path.startswith("/admin"):
        return await call_next(request)

    if (
        request.url.path.startswith("/auth")
        or request.url.path.startswith("/ws")
        or request.url.path.startswith("/interests")
    ):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header"
        )

    token = auth_header.split(" ")[1]
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    try:
        user = await get_current_user_from_token(token)
        request.state.user = user
        return await call_next(request)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Админ-панель роутер
admin_router = APIRouter()

# HTML для админ-панели (будет добавлен ниже)
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f9;
            color: #2c3e50;
        }
        .container {
            display: flex;
            min-height: 100vh;
            flex-direction: row;
        }
        .sidebar {
            width: 250px;
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
            overflow-y: auto;
        }
        .sidebar h2 {
            margin-top: 0;
            font-size: 1.5em;
        }
        #collections-list {
            list-style: none;
            padding: 0;
        }
        #collections-list li {
            padding: 10px;
            cursor: pointer;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        #collections-list li:hover {
            background-color: #34495e;
        }
        #collections-list li.active {
            background-color: #3498db;
        }
        .main-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        h1 {
            margin-bottom: 20px;
        }
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }
        #filter-input {
            padding: 10px;
            width: 300px;
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        .document-card {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
            padding: 15px;
        }
        .document-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        .document-header h3 {
            margin: 0;
            font-size: 1.2em;
            color: #3498db;
        }
        .document-content {
            display: none;
            margin-top: 10px;
        }
        .document-content.expanded {
            display: block;
        }
        .document-field {
            margin: 5px 0;
            word-break: break-word;
        }
        .document-field strong {
            color: #2c3e50;
        }
        .actions {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .actions button {
            padding: 5px 10px;
            font-size: 0.9em;
        }
        .actions button:nth-child(2) {
            background-color: #e74c3c;
        }
        .actions button:nth-child(2):hover {
            background-color: #c0392b;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            width: 500px;
            max-width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }
        .close {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 1.5em;
            cursor: pointer;
        }
        form div {
            margin-bottom: 15px;
        }
        form label {
            display: block;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        form input, form textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        /* Адаптивный дизайн */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                box-shadow: none;
            }
            .main-content {
                padding: 10px;
            }
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            #filter-input {
                width: 100%;
            }
            .document-header h3 {
                font-size: 1em;
            }
            .modal-content {
                width: 90%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>Collections</h2>
            <ul id="collections-list"></ul>
        </div>
        <div class="main-content">
            <h1>Admin Panel</h1>
            <div class="controls">
                <button onclick="showAddDocumentForm()">Add Document</button>
                <input type="text" id="filter-input" placeholder="Filter documents..." onkeyup="filterDocuments()">
            </div>
            <div id="documents-list"></div>
        </div>
        <div id="add-modal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeAddModal()">×</span>
                <h2>Add New Document</h2>
                <form id="add-form" onsubmit="addDocument(event)">
                    <div id="add-form-fields"></div>
                    <button type="submit">Add</button>
                </form>
            </div>
        </div>
        <div id="edit-modal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeEditModal()">×</span>
                <h2>Edit Document</h2>
                <form id="edit-form" onsubmit="updateDocument(event)">
                    <div id="edit-form-fields"></div>
                    <button type="submit">Update</button>
                </form>
            </div>
        </div>
    </div>
    <script>
        let currentCollection = null;
        let documents = [];
        let sortBy = null;
        let sortOrder = "asc";

        document.addEventListener("DOMContentLoaded", async () => {
            await loadCollections();
        });

        // Загрузка списка коллекций
        async function loadCollections() {
            const response = await fetch("/admin/collections");
            const data = await response.json();
            const collectionsList = document.getElementById("collections-list");
            collectionsList.innerHTML = "";
            data.collections.forEach(collection => {
                const li = document.createElement("li");
                li.textContent = collection;
                li.onclick = () => selectCollection(collection);
                collectionsList.appendChild(li);
            });
        }

        // Выбор коллекции
        async function selectCollection(collection) {
            currentCollection = collection;
            document.querySelectorAll("#collections-list li").forEach(li => li.classList.remove("active"));
            event.target.classList.add("active");
            await loadDocuments();
        }

        // Загрузка документов
        async function loadDocuments() {
            if (!currentCollection) return;
            const url = sortBy ? `/admin/collections/${currentCollection}?sort_by=${sortBy}&sort_order=${sortOrder}` : `/admin/collections/${currentCollection}`;
            const response = await fetch(url);
            const data = await response.json();
            documents = data.documents;
            displayDocuments(documents);
        }

        // Отображение документов в виде карточек
        function displayDocuments(docs) {
            const documentsList = document.getElementById("documents-list");
            documentsList.innerHTML = "";

            if (docs.length === 0) {
                documentsList.innerHTML = "<p>No documents found.</p>";
                return;
            }

            docs.forEach(doc => {
                const card = document.createElement("div");
                card.className = "document-card";

                const header = document.createElement("div");
                header.className = "document-header";
                const title = document.createElement("h3");
                title.textContent = doc._id || "Document";
                const toggleBtn = document.createElement("button");
                toggleBtn.textContent = "Expand";
                toggleBtn.onclick = () => toggleDocument(card, toggleBtn);

                header.appendChild(title);
                header.appendChild(toggleBtn);

                const content = document.createElement("div");
                content.className = "document-content";
                Object.entries(doc).forEach(([key, value]) => {
                    const field = document.createElement("div");
                    field.className = "document-field";
                    field.innerHTML = `<strong>${key}:</strong> ${typeof value === "object" ? JSON.stringify(value) : value}`;
                    content.appendChild(field);
                });

                const actions = document.createElement("div");
                actions.className = "actions";
                const editBtn = document.createElement("button");
                editBtn.textContent = "Edit";
                editBtn.onclick = () => showEditDocumentForm(doc);
                const deleteBtn = document.createElement("button");
                deleteBtn.textContent = "Delete";
                deleteBtn.onclick = () => deleteDocument(doc._id);
                actions.appendChild(editBtn);
                actions.appendChild(deleteBtn);
                content.appendChild(actions);

                card.appendChild(header);
                card.appendChild(content);
                documentsList.appendChild(card);
            });
        }

        // Сворачивание/разворачивание документа
        function toggleDocument(card, toggleBtn) {
            const content = card.querySelector(".document-content");
            if (content.classList.contains("expanded")) {
                content.classList.remove("expanded");
                toggleBtn.textContent = "Expand";
            } else {
                content.classList.add("expanded");
                toggleBtn.textContent = "Collapse";
            }
        }

        // Сортировка документов
        async function sortDocuments(field) {
            if (sortBy === field) {
                sortOrder = sortOrder === "asc" ? "desc" : "asc";
            } else {
                sortBy = field;
                sortOrder = "asc";
            }
            await loadDocuments();
        }

        // Фильтрация документов
        function filterDocuments() {
            const filter = document.getElementById("filter-input").value.toLowerCase();
            const filteredDocs = documents.filter(doc =>
                Object.values(doc).some(val =>
                    String(val).toLowerCase().includes(filter)
                )
            );
            displayDocuments(filteredDocs);
        }

        // Показать форму добавления документа
        function showAddDocumentForm() {
            if (!currentCollection) {
                alert("Please select a collection first.");
                return;
            }
            const modal = document.getElementById("add-modal");
            const fieldsContainer = document.getElementById("add-form-fields");
            fieldsContainer.innerHTML = "";
            
            if (documents.length > 0) {
                Object.keys(documents[0]).forEach(key => {
                    if (key === "_id") return;
                    const div = document.createElement("div");
                    const label = document.createElement("label");
                    label.textContent = key;
                    const input = document.createElement("input");
                    input.name = key;
                    input.placeholder = `Enter ${key}`;
                    div.appendChild(label);
                    div.appendChild(input);
                    fieldsContainer.appendChild(div);
                });
            } else {
                const div = document.createElement("div");
                const label = document.createElement("label");
                label.textContent = "Document JSON";
                const textarea = document.createElement("textarea");
                textarea.name = "json";
                textarea.placeholder = '{"key": "value"}';
                textarea.style.width = "100%";
                textarea.style.height = "200px";
                div.appendChild(label);
                div.appendChild(textarea);
                fieldsContainer.appendChild(div);
            }
            modal.style.display = "flex";
        }

        // Закрыть форму добавления
        function closeAddModal() {
            document.getElementById("add-modal").style.display = "none";
        }

        // Добавить документ
        async function addDocument(event) {
            event.preventDefault();
            const form = document.getElementById("add-form");
            const formData = new FormData(form);
            let data = {};
            
            if (documents.length > 0) {
                for (let [key, value] of formData.entries()) {
                    try {
                        data[key] = JSON.parse(value);
                    } catch (e) {
                        data[key] = value;
                    }
                }
            } else {
                const jsonStr = formData.get("json");
                try {
                    data = JSON.parse(jsonStr);
                } catch (e) {
                    alert("Invalid JSON format");
                    return;
                }
            }

            const response = await fetch(`/admin/collections/${currentCollection}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ data })
            });
            if (response.ok) {
                closeAddModal();
                await loadDocuments();
            } else {
                alert("Error adding document");
            }
        }

        // Показать форму редактирования
        function showEditDocumentForm(doc) {
            const modal = document.getElementById("edit-modal");
            const fieldsContainer = document.getElementById("edit-form-fields");
            fieldsContainer.innerHTML = "";
            document.getElementById("edit-form").dataset.id = doc._id;

            Object.keys(doc).forEach(key => {
                if (key === "_id") return;
                const div = document.createElement("div");
                const label = document.createElement("label");
                label.textContent = key;
                const input = document.createElement("input");
                input.name = key;
                input.value = typeof doc[key] === "object" ? JSON.stringify(doc[key]) : doc[key];
                div.appendChild(label);
                div.appendChild(input);
                fieldsContainer.appendChild(div);
            });
            modal.style.display = "flex";
        }

        // Закрыть форму редактирования
        function closeEditModal() {
            document.getElementById("edit-modal").style.display = "none";
        }

        // Обновить документ
        async function updateDocument(event) {
            event.preventDefault();
            const form = document.getElementById("edit-form");
            const docId = form.dataset.id;
            const formData = new FormData(form);
            let data = {};

            for (let [key, value] of formData.entries()) {
                try {
                    data[key] = JSON.parse(value);
                } catch (e) {
                    data[key] = value;
                }
            }

            const response = await fetch(`/admin/collections/${currentCollection}/${docId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ data })
            });
            if (response.ok) {
                closeEditModal();
                await loadDocuments();
            } else {
                alert("Error updating document");
            }
        }

        // Удалить документ
        async function deleteDocument(docId) {
            if (!confirm("Are you sure you want to delete this document?")) return;
            const response = await fetch(`/admin/collections/${currentCollection}/${docId}`, {
                method: "DELETE"
            });
            if (response.ok) {
                await loadDocuments();
            } else {
                alert("Error deleting document");
            }
        }
    </script>
</body>
</html>
"""


@admin_router.get("/", response_class=HTMLResponse)
async def admin_panel():
    return ADMIN_HTML


# Получение списка коллекций
@admin_router.get("/collections")
async def get_collections():
    collections = await db_service.db.list_collection_names()
    return {"collections": collections}


# Получение документов из коллекции
@admin_router.get("/collections/{collection_name}")
async def get_documents(
    collection_name: str,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
):
    try:
        collection = db_service.db[collection_name]
        cursor = collection.find()

        # Сортировка, если указаны параметры
        if sort_by:
            sort_direction = 1 if sort_order == "asc" else -1
            cursor = cursor.sort(sort_by, sort_direction)

        documents = await cursor.to_list(length=None)
        # Преобразуем ObjectId в строку для корректной сериализации
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            # Преобразуем вложенные ObjectId, если есть
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
                elif isinstance(value, list):
                    doc[key] = [
                        str(item) if isinstance(item, ObjectId) else item
                        for item in value
                    ]
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Модель для создания/обновления документа
class DocumentData(BaseModel):
    data: Dict[str, Any]


# Добавление документа
@admin_router.post("/collections/{collection_name}")
async def add_document(collection_name: str, doc: DocumentData):
    try:
        collection = db_service.db[collection_name]
        result = await collection.insert_one(doc.data)
        return {"inserted_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Обновление документа
@admin_router.put("/collections/{collection_name}/{doc_id}")
async def update_document(collection_name: str, doc_id: str, doc: DocumentData):
    try:
        collection = db_service.db[collection_name]
        result = await collection.update_one(
            {"_id": ObjectId(doc_id)}, {"$set": doc.data}
        )
        return {"modified_count": result.modified_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Удаление документа
@admin_router.delete("/collections/{collection_name}/{doc_id}")
async def delete_document(collection_name: str, doc_id: str):
    try:
        collection = db_service.db[collection_name]
        result = await collection.delete_one({"_id": ObjectId(doc_id)})
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Подключение админ-роутера
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Остальные маршруты без изменений
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(
    recommendations_router, prefix="/recommendations", tags=["Recommendations"]
)
app.include_router(group_tours_router, prefix="/group-tours", tags=["Group Tours"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(interests_router, prefix="/interests", tags=["Interests"])

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
