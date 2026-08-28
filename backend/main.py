from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import chat_router
import uvicorn

app = FastAPI(
    title="Real-Time Asynchronous Chatbot API",
    description="WebSocket streaming session manager, conversational memory, and async message dispatcher.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "realtime-chatbot"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
