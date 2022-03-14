from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

import requests
import json
import re

client_id = 'YourClientId'
client_secret = 'YourClientSecret'
base_url = 'https://api.intra.42.fr/v2/'
core_request = 'campus/1/locations'
filter = '?filter[active]=true'

client = BackendApplicationClient(client_id=client_id)
api = OAuth2Session(client=client)
token = api.fetch_token(token_url='https://api.intra.42.fr/oauth/token', client_id=client_id, client_secret=client_secret)

page = 0
first = True
while first or len(users) == 100:
    first = False
    requeststr = base_url + core_request + filter + '&page[size]=100&page[number]=' + str(page)
    response = api.get(requeststr)
    if(response.status_code != 200):
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
