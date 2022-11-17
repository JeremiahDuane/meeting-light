#!/usr/bin/env python
import time
import sys
import webbrowser

#local
from identifiers import identifiers
from gateway import SendMessage
from calendars import GetCurrentEvents

ON = True
IS_BUSY = False
IS_FREE = False

def CheckIsBusy():
    events = GetCurrentEvents()

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
    SendMessage(identifiers["busy"])

def HandleFree():
    SendMessage(identifiers["free"])

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
