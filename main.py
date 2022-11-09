#!/usr/bin/env python
import time
import datetime
import sys

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

def GetSchedulesForDay():
    schedules = []

    return schedules

def EscapeEvent(id):
    ESCAPED_EVENTS.append(id)

def CheckIsBusy():
    for schedule in GetSchedulesForDay():
        if schedule.isCurrent():
            return True
    return False

def HandleSchedule():
    if CheckIsBusy():
        Emit(GREEN)
    else:
        Emit(RED)

def Emit(color):
    return False

try:
    print("Press CTRL-C to stop.")
    while ON:
        time.sleep(.25)
        HandleSchedule()
except KeyboardInterrupt:
    sys.exit(0)