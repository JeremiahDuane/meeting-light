#!/usr/bin/env python
import time
import sys
import os
import json
import pytz
import socket
import recurring_ical_events
import icalendar
import ics
import webbrowser
import requests
import scapy.all as scapy

from directories import DIRECTORIES
from datetime import datetime

ON = True
IS_BUSY = False
IS_FREE = False
BUSY_IDENTIFIER = "RED"
FREE_IDENTIFIER = "GREEN"
OTHER_IDENTIFIER = "BLUE"

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

def HandleSchedule():
    global IS_FREE
    global IS_BUSY
    if CheckIsBusy():
        if not IS_BUSY:
            HandleBusy()
            IS_BUSY = True
            IS_FREE = False
    elif IS_BUSY or not IS_FREE:
        HandleFree()
        IS_BUSY = False    
        IS_FREE = True 

def HandleBusy():
    #webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    SendMessage(BUSY_IDENTIFIER)

def HandleFree():
    SendMessage(FREE_IDENTIFIER)

#Communications
def SendMessage(message):
    port = "8787"
    with open("./bin/addresses.txt", "r") as f:
        for address in f:
            print("http://" + address + ":" + port + "/" + message)
            try:
                r = requests.post("http://" + address + ":" + port + "/" + message)
                r.close()
            except requests.exceptions.ConnectionError:
                continue

#Main
def Main():
    try:
        print("Press CTRL-C to stop.")
        while ON:
            HandleSchedule()
            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    Main()
