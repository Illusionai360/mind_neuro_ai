import streamlit as st
import requests
from datetime import datetime

API = "http://127.0.0.1:8000/api"


# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Mind Neuro AI", page_icon="🧠", layout="wide")

# ------------------- CUSTOM CSS -------------------
st.markdown("""
<style>
/* ========== GLOBAL LIGHT GRADIENT THEME ========== */
.stApp {
    background: linear-gradient(135deg, #f7c4d4 0%, #d6a4e3 50%, #fbc2eb 100%);
    background-attachment: fixed;
    color: #2d2d2d;
    font-family: 'Inter', sans-serif;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.6);
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(12px);
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

/* Sidebar title */
.sidebar-title {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    color: #7b2cbf;
    padding: 10px 0;
}

/* New Chat button */
.stButton>button {
    background: linear-gradient(90deg, #ff6b6b, #d94a97);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 8px 0;
    width: 100%;
    font-size: 16px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #d94a97, #ff6b6b);
    box-shadow: 0 0 8px rgba(217, 74, 151, 0.6);
    transform: translateY(-1px);
}

/* Chat History items */
.chat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(90deg, #f8a5c2, #d6a4e3);
    padding: 8px 10px;
    margin: 8px 0;
    border-radius: 12px;
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.chat-item:hover {
    background: linear-gradient(90deg, #d6a4e3, #f8a5c2);
    transform: translateX(2px);
}

/* 3 dots menu */
.chat-menu {
    color: white;
    font-size: 18px;
    cursor: pointer;
    padding: 0 6px;
}

/* Chat Bubbles */
.bot-bubble {
    background: linear-gradient(135deg, #f0d9ff, #d6a4e3);
    color: #2d2d2d;
    padding: 12px;
    border-radius: 14px 14px 14px 0;
    margin: 8px 0;
    max-width: 75%;
    box-shadow: 0 0 10px rgba(214, 164, 227, 0.3);
}

.user-bubble {
    background: linear-gradient(135deg, #ffb6c1, #f78ca0);
    color: #2d2d2d;
    padding: 12px;
    border-radius: 14px 14px 0 14px;
    margin: 8px 0;
    margin-left: auto;
    max-width: 75%;
    box-shadow: 0 0 10px rgba(255, 182, 193, 0.3);
}

/* Input box */
.stChatInput>div {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 182, 193, 0.4);
    border-radius: 25px;
    padding: 8px 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stChatInput input {
    background: transparent;
    color: #2d2d2d;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🧠 Illusion AI</div>", unsafe_allow_html=True)

    # New chat button
    if st.button("➕ New Chat"):
        try:
            r = requests.post(f"{API}/chats/new")
            st.session_state["active_chat"] = r.json()["id"]
            st.session_state["messages"] = []
        except:
            st.error("Unable to create a new chat")

    st.markdown("---")
    st.subheader("Chat History")

    try:
        chats = requests.get(f"{API}/chats").json()
    except:
        chats = []

    if "active_chat" not in st.session_state and chats:
        st.session_state["active_chat"] = chats[0]["id"]

    # Chat history with rename/delete
    for c in chats:
        chat_id = c["id"]

        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            if st.button(f"{c['title']}", key=f"chat-{chat_id}", use_container_width=True):
                st.session_state["active_chat"] = chat_id
                st.session_state["messages"] = []

        with col2:
            if st.button("⋮", key=f"menu-{chat_id}"):
                st.session_state["menu_open"] = chat_id

        if st.session_state.get("menu_open") == chat_id:
            new_name = st.text_input("Rename chat", value=c['title'], key=f"rename-{chat_id}")
            col_a, col_b = st.columns(2)

            with col_a:
                if st.button("Save", key=f"save-{chat_id}"):
                    requests.put(f"{API}/chats/{chat_id}", json={"title": new_name})
                    st.session_state["menu_open"] = None
                    st.rerun()

            with col_b:
                if st.button("Delete", key=f"delete-{chat_id}"):
                    requests.delete(f"{API}/chats/{chat_id}")
                    st.session_state["menu_open"] = None
                    if st.session_state.get("active_chat") == chat_id:
                        st.session_state["active_chat"] = None
                    st.rerun()

# ------------------- MAIN CHAT AREA -------------------
st.title("🧠 Mind Neuro AI ")
st.caption("AI Psychologist • Neurology • Psychology • Philosophy")

active = st.session_state.get("active_chat")
if not active:
    st.info("Click **New Chat** to start.")
    st.stop()

# Load chat messages
if "messages" not in st.session_state or not st.session_state["messages"]:
    thread = requests.get(f"{API}/chats/{active}").json()
    st.session_state["messages"] = thread["messages"]

# Render chat
for m in st.session_state["messages"]:
    role_class = "user-bubble" if m["role"] == "user" else "bot-bubble"
    st.markdown(f"<div class='{role_class}'>{m['content']}</div>", unsafe_allow_html=True)

# Sending chat message
user_input = st.chat_input("Type your message here...")
if user_input:
    data = {"chat_id": active, "content": user_input}
    
    r = requests.post(f"{API}/chat", data=data).json()  # FIXED: data instead of json

    # Append user message locally
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input,
        "id": -1,
        "created_at": str(datetime.utcnow())
    })
    
    # Append AI response
    st.session_state["messages"].append(r)

    st.rerun()
