from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json
from backend.app.schemas.chat_schema import ChatMessagePayload, ChatResponse, SessionHistoryResponse
from backend.app.services.chat_service import chat_engine

router = APIRouter(prefix="/api/v1/chat", tags=["Real-Time Chatbot"])

@router.post("/message", response_model=ChatResponse)
async def send_message(payload: ChatMessagePayload):
    try:
        result = await chat_engine.generate_response(payload.session_id, payload.user_id, payload.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}", response_model=SessionHistoryResponse)
async def get_history(session_id: str):
    history = chat_engine.get_session_history(session_id)
    return SessionHistoryResponse(session_id=session_id, total_messages=len(history), messages=history)

@router.websocket("/ws/{session_id}")
async def chat_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:
        while True:
            raw_text = await websocket.receive_text()
            try:
                data = json.loads(raw_text)
                user_msg = data.get("message", "")
                user_id = data.get("user_id", "anonymous_user")
                response = await chat_engine.generate_response(session_id, user_id, user_msg)
                await websocket.send_text(json.dumps({"status": "SUCCESS", "payload": response}))
            except json.JSONDecodeError:
                continue
    except WebSocketDisconnect:
        pass
