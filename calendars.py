#LIBRARIES
import recurring_ical_events
import icalendar
import os
import pytz
from datetime import datetime, timedelta

#LOCAL
from directories import DIRECTORIES

##
#*    Read all .ics files from the list of directories and combine 
#*    events into a single calendar object.
##
def GetCalendars(directories):
    calendars = []
    for dir in directories:
        for filename in os.listdir(dir):
            if filename.find(".ics") == -1:
                continue
            path = os.path.join(dir, filename)
            # checking if it is a file
            if os.path.isfile(path):
                with open(path) as file:
                    contents = file.read()
                    cal = icalendar.Calendar.from_ical(contents)
                    calendars.append(cal)
    return calendars

##
#*    Get all current calendar events (now + 5 minute buffer) 
##
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
            if nowUTC > (start - timedelta(minutes=5)) and nowUTC < end:
                currentEvents.append(event)
    return currentEvents
