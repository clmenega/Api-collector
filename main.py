import genericpath
from datetime import datetime, timedelta
from os import path

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from TokenManager import TokenManager
from Collector import Collector
from AWSManager import AWSManager
from ApiManager import ApiManager
import requests
import json
import re
import time

client_id = 'YourClientId'
client_secret = 'YourClientSecret'
base_url = 'https://api.intra.42.fr/v2/'
filter = '?filter[active]=true'


def convert_seconds_to_minutes(seconds: int) -> str:
    return time.strftime("%M:%S", time.gmtime(seconds))


def create_new_token() -> str:
    client_id = input('client_id:')
    client_secret = input('client_secret:')
    print(client_id)
    print(client_secret)
    token_manager = TokenManager()
    token = token_manager.get_new_token(client_id, client_secret)
    print("Your token have been created and will expire " + token_manager.get_expire_date(token, '%A %d %B at %H:%M:%S'))
    return token


def print_users(users):
    for user in users:
        print('floor: ' + user["floor"])
        print('rank: ' + user["rank"])
        print('station: ' + user["station"])
        print('Id: ' + str(user["Id"]))
        print('login: ' + user["login"])
        print('Host: ' + user["host"])
        print('Beginning: ' + user["Beginning"])
        print('Finish: ' + str(user["Finish"]))
        print('Date: ' + str(user["Date"]))
        print("-----------------------------------------")


def setup_token() -> str:
    # Check if Token is present and Valid
    token_manager = TokenManager()
    if not token_manager.token_is_valid():
        print("Your token is out of date please enter credential to get a new one")
        token = create_new_token()
    else:
        token = token_manager.get_stored_token()
        token_ttl = token_manager.get_ttl(token)
        if token_ttl < 600:
            print("Your Token will expire in " + convert_seconds_to_minutes(token_ttl))
            user_response = ''
            while user_response not in ["y", "n", "yes", "no"]:
                user_response = input("Do you want to create a new token ? y/n")
                user_response = user_response.lower()
            if user_response in ["y", "yes"]:
                token = create_new_token()
            else:
                print("Your Token will expire at " + token_manager.get_expire_date(token, "%H:%M:%S"))
    return token


access_token = setup_token()
collector = Collector(access_token)
# users = collector.get_active_now()
# print(users[0])
users = collector.get_new_connection_on_plage(datetime.now(), 900)
print_users(users)
# AWSManager.insert_connection(datetime.now(), users)
# print(type(users[0].keys()))
