# TailorTalk AI Assistant

A full-stack AI chat agent that books meetings on Google Calendar using:
- Google Gemini API (LLM)
- FastAPI backend server
- Streamlit chat interface
- Google Calendar Service Account

---

## 📌 Project Structure


---

## 🚀 How It Works

1. User opens the Streamlit app and types: *“Book a meeting tomorrow at 5pm.”*
2. Streamlit sends the message to the FastAPI backend.
3. FastAPI asks Gemini to check the user’s intent.
4. If the intent is `BOOK`, FastAPI calls Google Calendar API using the Service Account key.
5. The bot replies with a valid Google Calendar event link in the chat.

---

## ✅ `.env` Example

Create a `.env` file in your project root:

```env
GOOGLE_APPLICATION_CREDENTIALS=service_account.json
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

✅ How To Run Locally
pip install -r requirements.txt
uvicorn app.main:app --reload
streamlit run frontend.py
⚙️ Important: Calendar Sharing
To see the event in your real Google Calendar:

Go to Google Calendar → Settings → Share with specific people.

Add your Service Account’s client_email from service_account.json.

Give it Make changes to events permission.

Use calendarId='your_email@gmail.com' in create_event() if needed.
