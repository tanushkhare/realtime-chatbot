# In-memory storage for chat sessions
chat_sessions = {}

def process_chat_message(session_id: str, message: str):
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    history = chat_sessions[session_id]
    
    # Generate bot reply based on message
    reply = f"Echo/Response to: '{message}'. (Processed with context length {len(history)})"
    
    # Append to history
    history.append({"user": message, "bot": reply})
    
    return {
        "session_id": session_id,
        "response": reply,
        "history_length": len(history)
    }