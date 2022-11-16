import recurring_ical_events
import icalendar
import os
import pytz
from datetime import datetime, timedelta

#Local
from directories import DIRECTORIES

def GetCalendars(directories):
    calendars = []
    for dir in directories:
        for filename in os.listdir(dir):
            if filename.find(".DS_Store") != -1:
                continue
            path = os.path.join(dir, filename)
            # checking if it is a file
            if os.path.isfile(path):
                with open(path) as file:
                    contents = file.read()
                    cal = icalendar.Calendar.from_ical(contents)
                    calendars.append(cal)
    return calendars

def GetCurrentEvents():
    currentEvents = []
    directories = DIRECTORIES
    calendars = GetCalendars(directories)
    now = datetime.now()

    nowUTC = datetime.now().astimezone(pytz.UTC)
    for cal in calendars:
        for event in recurring_ical_events.of(cal).at((now.year, now.month, now.day)):
            start = event.get("dtstart").dt.astimezone(pytz.UTC)
            end = event.get("dtend").dt.astimezone(pytz.UTC)
            print(str(nowUTC) + ":" + str(start) + " . " + str(end))
            if nowUTC > (start - timedelta(minutes=5)) and nowUTC < end:
                currentEvents.append(event)
    return currentEvents
