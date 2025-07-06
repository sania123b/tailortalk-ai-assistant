from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=credentials)

def create_event(summary, start_time, end_time, description="", attendees=[]):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }

    if attendees:
        event['attendees'] = attendees

    created_event = service.events().insert(
        calendarId='1a47e2f06ad9ef9f3644d97c75f548d20f969e6f12facae49ea496fdcaa2ce18@group.calendar.google.com',
        body=event
    ).execute()

    return created_event.get('htmlLink')
