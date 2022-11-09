#!/usr/bin/env python
import time
from datetime import datetime
import sys
import os
import json
import pytz

import recurring_ical_events
import icalendar
import ics

from directories import DIRECTORIES

GREEN = "Green"
RED = "Red"
ON = True
ESCAPED_EVENTS = []

class ScheduledEvent():
    def __init__(self,id, start, end):
        self.id = id
        self.start = start
        self.end = end
    def isCurrent(self):
        now = datetime.now()
        return self.start >= now and self.end < now

def GetCalendar(directories):
    calendar = icalendar.Calendar()
    for dir in directories:
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            # checking if it is a file
            if os.path.isfile(path):
                with open(path) as file:
                    contents = file.read()
                    cal = icalendar.Calendar.from_ical(contents)
                    for component in cal.walk():
                        if component.name == "VEVENT":
                            event = icalendar.Event()
                            event.add('name', component.get("name"))
                            event.add('description', component.get("description"))
                            start = component.decoded("dtstart")
                            end = component.decoded("dtend")
                            if isinstance(start, datetime) and isinstance(end, datetime):
                                event.add('dtstart', start.astimezone(pytz.UTC))
                                event.add('dtend', end.astimezone(pytz.UTC))
                            else:
                                event.add('dtstart', start)
                                event.add('dtend', end)
                            calendar.add_component(event)
    return calendar

def EscapeEvent(id):
    ESCAPED_EVENTS.append(id)

def HandleSchedule():
    if CheckIsBusy():
        Emit(GREEN)
    else:
        Emit(RED)

def Emit(color):
    return False

def CheckIsBusy():
    directories = DIRECTORIES
    calendar = GetCalendar(directories)
    now = datetime.now().astimezone(pytz.UTC)
    events = recurring_ical_events.of(calendar).at((now.year, now.month, now.day, now.hour, now.minute))
    # for event in events:
    #     start = event["DTSTART"].dt
    #     duration = event["DTEND"].dt - event["DTSTART"].dt
    #     print("start {} duration {}".format(start, duration))

    if len(events) > 0:
        return True
    else:
        return False

print(CheckIsBusy())
# try:
#     print("Press CTRL-C to stop.")
#     while ON:
#         time.sleep(.25)
#         HandleSchedule()
# except KeyboardInterrupt:
#     sys.exit(0)



