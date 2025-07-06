import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Google Calendar scope
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    """
    Creates the Google Calendar service client.
    Always overwrite service_account.json to guarantee valid PEM.
    """

    # ✅ Always overwrite — avoid stale/broken PEM
    if os.getenv("GOOGLE_CREDENTIALS"):
        creds_json = os.environ["GOOGLE_CREDENTIALS"].replace('\\n', '\n')
        with open(SERVICE_ACCOUNT_FILE, "w") as f:
            f.write(creds_json)

        # ✅ Debug: show first part of written file
        print("----- DEBUG: service_account.json written -----")
        with open(SERVICE_ACCOUNT_FILE) as f:
            print(f.read()[:300])  # Show only first 300 chars

    # ✅ Load credentials from the written file
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def create_event(summary, start_time, end_time):
    """
    Creates a new Google Calendar event.
    Returns the HTML link to view the event.
    """
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }

    # ✅ Use your calendar ID — make sure service account has permission!
    created_event = service.events().insert(
        calendarId='1a47e2f06ad9ef9f3644d97c75f548d20f969e6f12facae49ea496fdcaa2ce18@group.calendar.google.com',
        body=event
    ).execute()

    return created_event.get('htmlLink')
