from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict

app = FastAPI(
    title="Vector RAG Q&A System API",
    version="1.0.0",
    description="Real-time chat and document retrieval backend."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for chat sessions
chat_sessions: Dict[str, List[Dict[str, str]]] = {}

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the chat session")
    message: str = Field(..., description="The user message to send to the chatbot")

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history_length: int

@app.get("/")
def read_root():
    return {"message": "Vector RAG Q&A System Backend is running successfully!"}

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    if payload.session_id not in chat_sessions:
        chat_sessions[payload.session_id] = []
    
    history = chat_sessions[payload.session_id]
    reply = f"Echo/Response to: '{payload.message}'. (Processed with context length {len(history)})"
    history.append({"user": payload.message, "bot": reply})
    
    return {
        "session_id": payload.session_id,
        "response": reply,
        "history_length": len(history)
    }