import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from fastapi import WebSocket

class ResilientChatConnectionManager:
    def __init__(self):
        # Room tracking: room_id -> list of active WebSockets
        self.rooms: Dict[str, List[WebSocket]] = {}
        # History tracking: room_id -> list of serialized message records
        self.room_history: Dict[str, List[Dict[str, Any]]] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = []
            self.room_history[room_id] = []
        self.rooms[room_id].append(websocket)

        # Replay room history to the newly connected peer for session recovery
        if self.room_history[room_id]:
            await websocket.send_text(json.dumps({
                "type": "CHAT_HISTORY_RECOVERY",
                "room_id": room_id,
                "messages": self.room_history[room_id]
            }))

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.rooms and websocket in self.rooms[room_id]:
            self.rooms[room_id].remove(websocket)
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, sender_ws: Optional[WebSocket], message_record: Dict[str, Any]):
        if room_id not in self.room_history:
            self.room_history[room_id] = []
        self.room_history[room_id].append(message_record)

        payload = json.dumps({
            "type": "CHAT_MESSAGE_BROADCAST",
            "data": message_record
        })

        if room_id in self.rooms:
            for peer in list(self.rooms[room_id]):
                try:
                    await peer.send_text(payload)
                except Exception:
                    self.disconnect(room_id, peer)

    def get_room_stats(self, room_id: str) -> Dict[str, Any]:
        peers = len(self.rooms.get(room_id, []))
        messages = len(self.room_history.get(room_id, []))
        return {
            "room_id": room_id,
            "active_peers": peers,
            "persisted_messages": messages,
            "status": "ACTIVE_ROOM" if peers > 0 else "IDLE_ROOM"
        }

chat_manager = ResilientChatConnectionManager()
