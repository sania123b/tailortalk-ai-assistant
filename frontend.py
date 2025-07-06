import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from app.calendar_utils import create_event
from datetime import datetime, timedelta

# Load env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Page config
st.set_page_config(
    page_title="TailorTalk AI",
    page_icon="📅",
    layout="centered"
)

# --------------------------
# Custom CSS
# --------------------------
st.markdown("""
    <style>
    body {
        background: #f1f3f4;
    }
    .hero {
        text-align: center;
        padding: 40px 0 10px 0;
    }
    .hero img {
        width: 120px;
    }
    .hero h1 {
        font-size: 38px;
        color: #1a73e8;
        margin-top: 20px;
        margin-bottom: 5px;
    }
    .hero p {
        font-size: 18px;
        color: #555;
    }
    .chat-container {
        background: white;
        border-radius: 12px;
        max-width: 750px;
        margin: auto;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
    }
    .chat-bubble {
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        line-height: 1.6;
        font-size: 16px;
    }
    .user {
        background: #e8f0fe;
        color: #174ea6;
    }
    .bot {
        background: #f1f8e9;
        color: #33691e;
    }
    .footer {
        text-align: center;
        color: #777;
        font-size: 13px;
        padding: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Hero section with Google Calendar logo
# --------------------------

st.markdown("""
    <div class='hero'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Google_Calendar_icon_%282020%29.svg/1024px-Google_Calendar_icon_%282020%29.svg.png' alt='Google Calendar Logo'>
        <h1>TailorTalk AI</h1>
        <p>Smart meeting booking with Google Calendar & Gemini</p>
    </div>
""", unsafe_allow_html=True)

# --------------------------
# Chat container
# --------------------------

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Say something like 'Book a meeting tomorrow...'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = model.generate_content(
        f"""
        Does the user want to book a meeting?
        "{user_input}"
        Reply ONLY with 'BOOK' or 'UNKNOWN'.
        """
    )

    intent = response.text.strip().upper()

    if "BOOK" in intent:
        now = datetime.utcnow()
        start = (now + timedelta(hours=1)).isoformat()
        end = (now + timedelta(hours=2)).isoformat()
        link = create_event("TailorTalk Booking", start, end)
        # ✅ Bot reply does NOT show the link
        bot_reply = "✅ Booking confirmed!"
        # ✅ Save link to session to show button below
        st.session_state.last_link = link
    else:
        bot_reply = "🤖 I didn't understand. Please say: 'Book a meeting tomorrow at 5pm'."
        st.session_state.last_link = None  # Clear any old link

    st.session_state.messages.append({"role": "bot", "content": bot_reply})

# --------------------------
# Show chat bubbles
# --------------------------

for msg in st.session_state.messages:
    bubble_class = "user" if msg["role"] == "user" else "bot"
    st.markdown(
        f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>",
        unsafe_allow_html=True
    )

# ✅ ✅ ✅ Show a separate button if there is a last link
if st.session_state.get("last_link"):
    st.link_button("🔗 View Event in Google Calendar", url=st.session_state.last_link)

st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# Footer
# --------------------------

st.markdown("""
    <div class='footer'>
        © 2025 TailorTalk | Google Calendar + Gemini | Internship Demo
    </div>
""", unsafe_allow_html=True)
