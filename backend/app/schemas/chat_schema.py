from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChatMessagePayload(BaseModel):
    session_id: str = Field(..., description="Unique conversation session ID")
    user_id: str = Field(..., description="Client user principal")
    message: str = Field(..., min_length=1, description="Message string")

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    tokens_generated: int
    latency_ms: float
    timestamp: str

class SessionHistoryResponse(BaseModel):
    session_id: str
    total_messages: int
    messages: List[Dict[str, Any]]
