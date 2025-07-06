import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Google Calendar scope
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    # ✅ FIX: Write the credentials file if missing
    if not os.path.exists(SERVICE_ACCOUNT_FILE) and os.getenv("GOOGLE_CREDENTIALS"):
        # Replace literal \n with real line breaks for the private key
        creds_json = os.environ["GOOGLE_CREDENTIALS"].replace('\\n', '\n')
        with open(SERVICE_ACCOUNT_FILE, "w") as f:
            f.write(creds_json)

    # Load credentials from the file
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
    # ✅ Make sure to use your actual Gmail ID here
    created_event = service.events().insert(
        calendarId='1a47e2f06ad9ef9f3644d97c75f548d20f969e6f12facae49ea496fdcaa2ce18@group.calendar.google.com',
        body=event
    ).execute()
    return created_event.get('htmlLink')
