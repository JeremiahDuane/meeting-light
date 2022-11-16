import requests

def SendMessage(message):
    port = "8787"
    with open("./bin/addresses.txt", "r+") as f:
        for address in f:
            url = f'http://{address.strip()}:{port}/{message}'
            print(url)
            r = requests.post(url)
            r.close()
