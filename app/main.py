from fastapi import FastAPI
from pydantic import BaseModel
from .calendar_utils import create_event

import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    user_msg = req.message

    # Call Gemini to interpret the user's message
    response = model.generate_content(
        f"""Extract the intent, date and time from this request:
        "{user_msg}"
        If it's about booking, reply like: 'BOOK'
        Else, reply 'UNKNOWN'.
        """
    )

    content = response.text.strip().upper()
    print("Gemini raw:", content)

    if "BOOK" in content:
        now = datetime.utcnow()
        start = (now + timedelta(hours=1)).isoformat()
        end = (now + timedelta(hours=2)).isoformat()
        link = create_event("Meeting booked by TailorTalk", start, end)
        return {"reply": f"✅ Booking confirmed! Event: {link}"}

    return {"reply": "I didn't understand. Please say 'book a meeting'."}
