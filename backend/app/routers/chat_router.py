import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from backend.app.schemas.chat_schema import ChatMessagePayload, ChatRoomStatus, ChatMessageRecord
from backend.app.services.chat_service import chat_manager

router = APIRouter(prefix="/api/v1/chat", tags=["Real-Time Chat Engine"])

@router.websocket("/ws/{room_id}")
async def websocket_chat_endpoint(websocket: WebSocket, room_id: str):
    await chat_manager.connect(room_id, websocket)
    try:
        while True:
            raw_text = await websocket.receive_text()
            try:
                frame = json.loads(raw_text)
                record = {
                    "message_id": f"MSG-{uuid.uuid4().hex[:8].upper()}",
                    "room_id": room_id,
                    "sender": frame.get("sender", "Anonymous"),
                    "message": frame.get("message", ""),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                await chat_manager.broadcast(room_id, websocket, record)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "MALFORMED_JSON_FRAME"}))
    except WebSocketDisconnect:
        chat_manager.disconnect(room_id, websocket)

@router.post("/message", response_model=ChatMessageRecord)
async def post_message_http(payload: ChatMessagePayload):
    record = {
        "message_id": f"MSG-{uuid.uuid4().hex[:8].upper()}",
        "room_id": payload.room_id,
        "sender": payload.sender,
        "message": payload.message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await chat_manager.broadcast(payload.room_id, None, record)
    return ChatMessageRecord(**record)

@router.get("/rooms/{room_id}", response_model=ChatRoomStatus)
async def get_room_metrics(room_id: str):
    return ChatRoomStatus(**chat_manager.get_room_stats(room_id))

@router.get("/rooms/{room_id}/messages", response_model=List[ChatMessageRecord])
async def get_room_messages(room_id: str):
    history = chat_manager.room_history.get(room_id, [])
    return [ChatMessageRecord(**m) for m in history]
