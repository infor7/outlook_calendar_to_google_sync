import datetime
import json
import logging
import os
import sys

from exchangelib import Credentials, Account, EWSDateTime, EWSTimeZone

logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class OutlookDownloader:
    def __init__(self):
        email = os.environ['OUTLOOK_EMAIL']
        password = os.environ['OUTLOOK_PASSWORD']
        credentials = Credentials(email, password)
        self.account = Account(email, credentials=credentials, autodiscover=True)

    def get_calendar_events(self):
        start = self.account.default_timezone.localize(EWSDateTime.now())
        end = start + datetime.timedelta(days=30)

        events = []

        unfolded_items = self.account.calendar.view(start=start, end=end)
        tz = EWSTimeZone.localzone()
        for item in unfolded_items:
            if "Canceled:" in item.subject:
                continue
            events.append({
                "start": str(item.start.astimezone(tz).isoformat()),
                "end": str(item.end.astimezone(tz).isoformat()),
                "required_attendees": str(item.required_attendees),
                "optional_attendees": str(item.optional_attendees),
                "location": str(item.location),
                "message": str(item.text_body),
                "subject": str(item.subject),
            })
            logging.info('Added "{}" event'.format(item.subject))
        return events

    def create_file_with_outlook_events(self):
        pathname = os.path.dirname(sys.argv[0])
        full_path = os.path.abspath(pathname)

        events = self.get_calendar_events()
        with open(full_path + '/outlook_dump', 'w') as fh:
            fh.write(json.dumps(events))

    def _get_formatted_start_date(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        return year, month, day

    def _get_formatted_end_date(self, number_of_days_from_now):
        now = self.account.default_timezone.localize(EWSDateTime.now())
        end = now + datetime.timedelta(days=number_of_days_from_now)
        year = end.year
        month = end.month
        day = end.day
        return year, month, day


if __name__ == '__main__':
    try:
        od = OutlookDownloader()
        od.create_file_with_outlook_events()
    except Exception as e:
        logging.error("Error occurs: {}".format(e))
