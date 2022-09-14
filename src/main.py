import datetime
import os

import fastapi
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

app = fastapi.FastAPI()


def create_token():
    if os.path.exists('credentials.json'):
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())


def current_time_start_of_day():
    today = datetime.datetime.now().date()
    value = datetime.datetime(year=today.year, month=today.month, day=today.day).isoformat() + 'Z'
    print(value)
    return value


def current_time_end_of_day():
    today = datetime.datetime.now().date()
    value = datetime.datetime(year=today.year, month=today.month, day=today.day,
                              hour=23, minute=59, second=59).isoformat() + 'Z'
    print(value)
    return value


if not os.path.exists("token.json"):
    create_token()


@app.get("/events/today")
async def list_today_events():
    events = get_events_of_today()

    if not events:
        print('No upcoming events found.')

    for event in events:
        print(event['summary'])

    return events


@app.get("/events/stand-up")
async def list_today_events():
    events = get_events_of_today()

    results = [event for event in events if 'Stand-Up' in event['summary']]

    return len(results) != 0


def get_events_of_today():
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary',
                                          timeMin=current_time_start_of_day(),
                                          timeMax=current_time_end_of_day(),
                                          maxResults=100,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
