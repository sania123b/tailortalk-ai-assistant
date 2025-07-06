
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    # ✅ Always create the file if missing
    if not os.path.exists(SERVICE_ACCOUNT_FILE) and os.getenv("GOOGLE_CREDENTIALS"):
        with open(SERVICE_ACCOUNT_FILE, "w") as f:
            f.write(os.environ["GOOGLE_CREDENTIALS"])

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def create_event(summary, start_time, end_time):
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(
        calendarId='YOUR_GMAIL_ID@gmail.com',  # ✅ Use your real Gmail ID
        body=event
    ).execute()
    return created_event.get('htmlLink')
