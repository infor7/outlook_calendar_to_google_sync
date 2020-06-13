import json
import logging
import os
import pickle
import sys

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tzlocal import get_localzone

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class GoogleCalendarFeeder:
    def __init__(self):
        pathname = os.path.dirname(sys.argv[0])
        self.full_path = os.path.abspath(pathname)

        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None

        if os.path.exists(self.full_path + '/token.pickle'):
            with open(self.full_path + '/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.full_path + '/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.full_path + '/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def create_events(self):
        calendar_id = os.environ['GOOGLE_CALENDAR']

        events = self.service.events().list(calendarId=calendar_id).execute()
        for event in events['items']:
            self.service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()

        body_of_events = self.create_body_of_events()

        for body_of_event in body_of_events:
            self.service.events().insert(calendarId=calendar_id, body=body_of_event).execute()
            logging.info("Event {} added to calendar".format(body_of_event['summary']))

    def create_body_of_events(self):
        event_list = []
        with open(self.full_path + '/outlook_dump', 'r') as fh:
            json_events = json.loads(fh.read())
        tz = get_localzone()
        formatted_events = []
        for event in json_events:
            formatted_events.append({
                'summary': event['subject'],
                'location': event['location'],
                'description': "{}\nRequired attendies{}".format(event['message'], event['required_attendees']),
                'start': {
                    'dateTime': event['start'],
                    'timeZone': tz.zone,
                },
                'end': {
                    'dateTime': event['end'],
                    'timeZone': tz.zone,
                },
            })

        return formatted_events


if __name__ == '__main__':
    gcf = GoogleCalendarFeeder()
    gcf.create_events()
