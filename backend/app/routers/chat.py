from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_chat_message

router = APIRouter(prefix="/api", tags=["Chat"])

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    return process_chat_message(payload.session_id, payload.message)