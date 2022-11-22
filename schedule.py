#!/usr/bin/env python
import time
import sys
import webbrowser

#LOCAL
from config import Identifiers
from gateway import SendMessage
from calendars import GetCurrentEvents

ON = True
IS_BUSY = False
IS_FREE = False

##check if there are any current events
def CheckIsBusy():
    events = GetCurrentEvents()

    if len(events) > 0:
       return True
    else:
        return False

##check to see if there is a change in statuses
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

##handle busy event
def HandleBusy():
    SendMessage(Identifiers["busy"])

##handle free event
def HandleFree():
    SendMessage(Identifiers["free"])

##
#*  Watch for changes in status and push updates to server.
##
def WatchCalendarUpdates():
    try:
        print("Press CTRL-C to stop.")
        while ON:
            HandleSchedule()
            time.sleep(60)
    except KeyboardInterrupt:
        sys.exit(0)

#MAIN
if __name__ == "__main__":
    WatchCalendarUpdates()
