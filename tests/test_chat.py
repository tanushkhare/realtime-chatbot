import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_send_message_and_history():
    session = "test_session_99"
    payload = {
        "session_id": session,
        "user_id": "test_user",
        "message": "Hello AI assistant!"
    }
    res = client.post("/api/v1/chat/message", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["session_id"] == session
    assert len(data["reply"]) > 5

    # Check history
    hist_res = client.get(f"/api/v1/chat/history/{session}")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total_messages"] >= 2
