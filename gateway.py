
#LIBRARIES
import requests

##
#*    Send supplied message to arduino
##
def SendMessage(message):
    with open("./bin/addresses.txt", "r+") as f:
        for address in f:
            url = f'http://{address.strip()}/{message}'
            print(url)
            r = requests.post(url)
            r.close()