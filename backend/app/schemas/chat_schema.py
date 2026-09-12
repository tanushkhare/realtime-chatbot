from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessagePayload(BaseModel):
    room_id: str = Field(default="general-room")
    sender: str = Field(..., min_length=1, description="Sender username or handle")
    message: str = Field(..., min_length=1, description="Message text payload")

class ChatRoomStatus(BaseModel):
    room_id: str
    active_peers: int
    persisted_messages: int
    status: str

class ChatMessageRecord(BaseModel):
    message_id: str
    room_id: str
    sender: str
    message: str
    timestamp: str
