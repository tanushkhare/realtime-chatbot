# ⚡ Async Real-Time Chatbot

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://realtime-chatbot-two.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://realtime-chatbot-two.vercel.app](https://realtime-chatbot-two.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Bi-directional WebSocket streaming conversational gateway with session lifecycles, heartbeat ping/pong monitoring, and async tokenized delta chunk delivery.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** WebSockets, FastAPI, Redis Cache, Python AsyncIO
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Session Lifecycle:** UUID-scoped in-memory / Redis pools preventing state leakage.
* **Idle Timeout:** 15-minute connection reclamation to protect server memory.
* **Error Boundaries:** Resilient handling for malformed JSON frames.

---

## 🚀 API Contracts
```http
WS /ws/chat/{session_id}

Client Inbound:
{
  "type": "USER_PROMPT",
  "content": "Explain decoupled async event loops in FastAPI"
}

Server Outbound:
{"type": "TOKEN_DELTA", "delta": "Decoupled "}
{"type": "TOKEN_DELTA", "delta": "event "}
{"type": "STREAM_END", "total_tokens": 42}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v