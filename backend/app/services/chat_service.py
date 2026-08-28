import asyncio
import time
from datetime import datetime, timezone
from typing import Dict, List, Any

class RealTimeChatEngine:
    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, Any]]] = {}

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.sessions.get(session_id, [])

    async def generate_response(self, session_id: str, user_id: str, message: str) -> Dict[str, Any]:
        start = time.perf_counter()
        
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        # Append user message
        user_msg = {
            "role": "user",
            "user_id": user_id,
            "text": message,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.sessions[session_id].append(user_msg)

        await asyncio.sleep(0.02) # Async non-blocking generation simulation
        
        # Heuristic contextual assistant generation
        msg_lower = message.lower()
        if "hello" in msg_lower or "hi" in msg_lower:
            reply = "Hello! I am your real-time asynchronous AI assistant. How can I assist you with your systems engineering or architecture questions today?"
        elif "status" in msg_lower or "health" in msg_lower:
            reply = "All backend microservice nodes and WebSocket connection pools are currently operational at sub-15ms latency."
        else:
            reply = f"Acknowledged query regarding '{message}'. Non-blocking asynchronous token dispatch completed successfully."

        ai_msg = {
            "role": "assistant",
            "user_id": "ai_agent",
            "text": reply,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.sessions[session_id].append(ai_msg)

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        
        return {
            "session_id": session_id,
            "reply": reply,
            "tokens_generated": len(reply.split()),
            "latency_ms": elapsed_ms,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

chat_engine = RealTimeChatEngine()
