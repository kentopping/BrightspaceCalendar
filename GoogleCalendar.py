from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta


class GoogleClient(object):
    def __init__(self, creds_location):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.service = self.authorize(creds_location)
        self.calendars = self.get_calendars()

    def authorize(self, creds_location):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../token.json'):
            creds = Credentials.from_authorized_user_file('../token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(creds_location, self.SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)
        return service

    def get_calendars(self):
        result = self.service.calendarList().list().execute()
        ret = {}
        for i in result['items']:
            if i['summary'] == "Theory" or i['summary'] == "Assignments" or i['summary'] == "Labs":
                ret[f"{i['summary']}"] = f"{i['id']}"
        return ret

    def erase_calendar(self, calendar_name):
        calendar_id = self.calendars.get(f'{calendar_name}')
        # gets all events by calendar id
        result = self.service.events().list(calendarId=calendar_id, timeZone="Canada/Eastern").execute()
        # clears events from calendar to refresh calendar
        for i in result['items']:
            self.service.events().delete(calendarId=calendar_id, eventId=i['id']).execute()

    def create_event(self, calendar_id, summary, end, start_time):
        end_time = start_time + timedelta(hours=end)
        timezone = 'Canada/Eastern'

        event = {
            'summary': f'{summary}',
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        self.service.events().insert(calendarId=calendar_id, body=event).execute()

    def create_calendars(self, calendar_name):
        for name in self.calendars:
            if name == calendar_name:
                return
        calendar = {
            'summary': f'{calendar_name}',
            'timeZone': 'Canada/Eastern'
        }
        created_calendar = self.service.calendars().insert(body=calendar).execute()

    def add_events(self, file, csv_name):
        for line in file:
            array = line.split(",")
            month = array[1][0:3]
            datetime_object = datetime.strptime(month, "%b")
            month_number = datetime_object.month
            year = int(array[0])
            day = int(array[2])
            time = array[3].split(":")
            hour = int(time[0])
            minute = time[1].split(" ")
            if minute[1] == "PM":
                hour += 12
            minute = int(minute[0])
            subject = array[4]
            if subject == "":
                subject = array[5]
            start_time = datetime(year, month_number, day, hour, minute, 0)
            self.create(f'{csv_name}', f'{subject}', 2, start_time)

    def create(self, calendar, name, duration, start):
        calendar_id = self.calendars.get(f'{calendar}')
        self.create_event(calendar_id, f'{name}', duration, start)
