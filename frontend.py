import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI Assistant", page_icon="🧵")

# Custom CSS for color and style
st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
    }
    .stChatMessage {
        background: #ffffff;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 10px 0;
    }
    .stUser {
        color: #000000;
        background: #d9f0ff;
    }
    .stBot {
        color: #000000;
        background: #e1ffe1;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ TailorTalk AI Assistant")
st.caption("Book your appointments with a colorful, chatty Gemini bot!")

# Session state to store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input at the bottom
prompt = st.chat_input("Say something...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send to FastAPI backend
    response = requests.post("http://127.0.0.1:8000/chat", json={"message": prompt})
    bot_reply = response.json()["reply"]

    # Add bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# Display all messages beautifully
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**You:** {msg['content']}")
    else:
        with st.chat_message("assistant"):
            st.markdown(f"**TailorTalk Bot:** {msg['content']}")
