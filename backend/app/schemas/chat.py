from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    message: str = Field(..., description="The user message to send to the chatbot")

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history_length: int