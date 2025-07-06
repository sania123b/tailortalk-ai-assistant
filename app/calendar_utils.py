import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    """
    ✅ ALWAYS write fresh service_account.json on every run.
    ✅ Guarantees the PEM is correct.
    """

    creds_json = os.environ["GOOGLE_CREDENTIALS"]

    # ✅ Must exist, fail fast if not
    if not creds_json:
        raise RuntimeError("GOOGLE_CREDENTIALS env is empty!")

    # ✅ Replace all literal \n with real line breaks
    creds_json = creds_json.replace('\\n', '\n')

    # ✅ Write it fresh — always, no conditions
    with open(SERVICE_ACCOUNT_FILE, "w") as f:
        f.write(creds_json)

    # ✅ Debug: show first part — must see BEGIN PRIVATE KEY
    print("----- DEBUG: PEM content -----")
    with open(SERVICE_ACCOUNT_FILE) as f:
        print(f.read()[:300])

    # ✅ Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)


def create_event(summary, start_time, end_time):
    """
    ✅ Create Google Calendar event
    """
    service = get_calendar_service()
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }

    created_event = service.events().insert(
        calendarId='1a47e2f06ad9ef9f3644d97c75f548d20f969e6f12facae49ea496fdcaa2ce18@group.calendar.google.com',
        body=event
    ).execute()

    return created_event.get('htmlLink')
