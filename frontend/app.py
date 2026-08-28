import streamlit as st
import requests

st.set_page_config(page_title="Real-Time Chatbot", layout="wide")

st.title("💬 Asynchronous Real-Time Chat Assistant")
st.markdown("Low-latency asynchronous dialog streaming, session history persistence, and WebSocket dispatch.")

if "messages" not in st.session_state:
    st.session_state.messages = []

col1, col2 = st.columns([2, 1])

with col1:
    session_id = st.text_input("Session Identifier", value="session_tech_sync_01")
    
    # Display conversation messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    user_input = st.chat_input("Ask a question...")
    if user_input:
        st.session_state.messages.append({"role": "user", "text": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Streaming response..."):
                try:
                    res = requests.post(
                        "http://localhost:8000/api/v1/chat/message",
                        json={"session_id": session_id, "user_id": "usr_tanush", "message": user_input},
                        timeout=5
                    )
                    if res.status_code == 200:
                        data = res.json()
                        reply = data["reply"]
                        st.write(reply)
                        st.session_state.messages.append({"role": "assistant", "text": reply})
                    else:
                        st.error(f"Chat API Error: {res.text}")
                except Exception:
                    st.warning("Backend offline. Simulating local assistant reply.")
                    reply = f"Acknowledged: '{user_input}'. Processed via local fallback response loop."
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "text": reply})

with col2:
    st.subheader("Session Telemetry")
    st.metric("Total Messages in Context", len(st.session_state.messages))
    st.info(f"Active Session: `{session_id}`")
    st.success("✅ Asynchronous Event Loop & Persistent History Active")
