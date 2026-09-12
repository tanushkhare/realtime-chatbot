# ⚡ Async Real-Time Chatbot

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://realtime-chatbot-two.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://realtime-chatbot-two.vercel.app](https://realtime-chatbot-two.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Bi-directional WebSocket conversational streaming engine with session lifecycle isolation, heartbeat monitoring, and token delta broadcasting.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** WebSockets, FastAPI, Redis, Python AsyncIO
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🚀 API Contracts
```http
WS /ws/chat/{session_id}
GET /health
```

---

## 💻 Local Quickstart
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v
```
