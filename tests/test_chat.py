import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_http_message_post_and_room_stats():
    payload = {
        "room_id": "test-chat-room",
        "sender": "TestUser",
        "message": "Hello world from PyTest suite"
    }
    res = client.post("/api/v1/chat/message", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "MSG-" in data["message_id"]
    assert data["sender"] == "TestUser"

    # Room stats check
    stats_res = client.get("/api/v1/chat/rooms/test-chat-room")
    assert stats_res.status_code == 200
    stats = stats_res.json()
    assert stats["persisted_messages"] >= 1

def test_websocket_malformed_json_guardrail():
    with client.websocket_connect("/api/v1/chat/ws/test-ws-channel") as ws:
        ws.send_text("MALFORMED_NON_JSON_PAYLOAD")
        reply = ws.receive_json()
        assert "error" in reply
        assert reply["error"] == "MALFORMED_JSON_FRAME"
