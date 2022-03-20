import genericpath

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from TokenManager import TokenManager
import requests
import json
import re
import time

client_id = 'YourClientId'
client_secret = 'YourClientSecret'
base_url = 'https://api.intra.42.fr/v2/'
core_request = 'campus/1/locations'
filter = '?filter[active]=true'


def convert_seconds_to_minutes(seconds: int) -> str:
    return time.strftime("%M:%S", time.gmtime(seconds))


def create_new_token() -> str:
    client_id = input('client_id:')
    client_secret = input('client_secret:')
    token = TokenManager.get_new_token(client_id, client_secret)
    print("Your token have been created and will expire " + TokenManager.get_expire_date(token, '%A %d %B at %H:%M:%S'))
    return token


# Check if Token is present and Valide
if not TokenManager.token_is_valid:
    print("Your token is out of date please enter credential to get a new one")
    token = create_new_token()
else:
    token = TokenManager.get_stored_token()
    token_ttl = TokenManager.get_ttl(token)
    if token_ttl < 600:
        print("Your Token will expire in " + convert_seconds_to_minutes(token_ttl))
        response = ''
        while response not in ["y", "n", "yes", "no"]:
            response = input("Do you want to create a new token ? y/n")
            response = response.lower()
        if response in ["y", "yes"]:
            token = create_new_token()
        else:
            print("Your Token will expire at " + TokenManager.get_expire_date(token, "%H:%M:%S"))
        
client = BackendApplicationClient(client_id=client_id)
api = OAuth2Session(client=client)
token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id,
                        client_secret=client_secret)

page = 0
first = True
while first or len(users) == 100:
    first = False
    requeststr = base_url + core_request + filter + '&page[size]=100&page[number]=' + str(page)
    response = api.get(requeststr)
    if (response.status_code != 200):
        print(response.status_code)
        print(response.reason)
        break
    users = json.loads(response.content)
    for user in users:
        match = re.match(r"[e]([1-3])[r](\d{1,2})[p](\d{1,2})", str(user["host"]))
        if match:
            print('floor: ' + match.group(1))
            print('rank: ' + match.group(2))
            print('station: ' + match.group(3))
            print('Id: ' + str(user["id"]))
            print('Host: ' + str(user["host"]))
            print('Beginig: ' + str(user["begin_at"]))
            print('Finish: ' + str(user["end_at"]))
            print("-----------------------------------------")
    page += 1
    print('page: ' + str(page))