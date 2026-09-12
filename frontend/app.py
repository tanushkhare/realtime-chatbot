import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Chatbot", layout="wide")

st.title("💬 Resilient Real-Time WebSocket Messaging Hub")
st.markdown("Non-blocking asynchronous room management, frame validation, and chat history persistence.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Transmit Chat Message")
    room_id = st.text_input("Channel / Room Identifier", value="sre-war-room")
    sender = st.text_input("Handle / Sender", value="Tanush Khare")
    msg = st.text_area("Message Payload", value="Deploying microservices across all clusters. Health checks nominal.")

    if st.button("Send Message via HTTP Dispatch", type="primary"):
        payload = {"room_id": room_id, "sender": sender, "message": msg}
        try:
            res = requests.post("http://localhost:8000/api/v1/chat/message", json=payload, timeout=5)
            if res.status_code == 200:
                st.session_state["p03a_last"] = res.json()
                st.success("Message dispatched to room broadcast!")
            else:
                st.error(f"Dispatch Error: {res.text}")
        except Exception:
            st.warning("Backend offline. Simulating local dispatch.")
            st.session_state["p03a_last"] = {
                "message_id": "MSG-SIM001",
                "room_id": room_id,
                "sender": sender,
                "message": msg,
                "timestamp": "2026-08-28T12:00:00Z"
            }

with col2:
    if "p03a_last" in st.session_state:
        r = st.session_state["p03a_last"]
        st.subheader(f"Dispatched Frame: {r['message_id']}")
        st.info(f"**{r['sender']}** in `#{r['room_id']}`:\n\n> {r['message']}")
        st.markdown(f"**Timestamp:** `{r['timestamp']}`")
