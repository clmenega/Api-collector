import datetime
import os.path as path
import os.listdir as listdir
import os.mkdir as mkdir
import os.remove as remove
import requests
import time
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from typing import Dict, Any

_TOKEN_DIR = '~/.Api_Collector'
_TOKEN_FILE_NAME = 'token.txt'
_FT_TOKEN_URL = "https://api.intra.42.fr/oauth/token"
_FT_TOKEN_INFO_URL = _FT_TOKEN_URL + "/info"
_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

JsonDict = Dict[str, Any]


# create directory if not exist
def _create_dir(dir_path) -> bool:
    if not path.isdir(dir_path):
        mkdir(path.expanduser(dir_path))


class TokenManager:
    def __init__(self, token_dir: str, _token_file_name):
        if not token_dir:
            self.token_dir = _TOKEN_DIR
        if not _token_file_name:
            self._token_file_name = _TOKEN_FILE_NAME
        _create_dir(self.token_dir)
        self._token_file_path = path.join(self.token_dir, self._token_file_name)


    def token_is_valid(self) -> bool:
        if self._token_file_exist():
            token = self._get_token_stored()
            return not self._token_is_outdate(token)
        return False

    # Store and return a new token
    def get_new_token(self, client_id, client_secret) -> str:
        token = self._get_new_token(client_id, client_secret)
        self._store_token(token)
        return token

    # Return a string with the expire date of the given token
    def get_expire_date(self, token: str, date_format: str) -> str:
        token_data = self._get_token_info(token)
        expire_seconds = int(token_data.expire_in_seconds)
        curent_date = datetime.datetime.now()
        expire_time = curent_date + datetime.timedelta(0, expire_seconds)
        return expire_time.strftime(date_format)

    def get_stored_token(self) -> str:
        self._get_token_stored()

    def get_ttl(self, token) -> int:
        token_data = self._get_token_info(token)
        return int(token_data.expire_in_seconds)


                ############################
                ### Token File Managment ###
                ############################

    # Return boolean on existence of file that store the token
    def _token_file_exist(self) -> bool:
        return path.exists(path.expanduser(self._token_file_path))

    #Read token from file
    def _get_token_stored(self) -> str:
        file = open(self._token_file_path, "r")
        return file.read()

    #Remove the file with token
    def _delete_token_stored(self) -> bool:
        if path.exists(self._token_file_path):
            remove(self._token_file_path)

    def _store_token(self, content) -> bool:
        if self._token_file_exist():
           self._delete_token_stored()
        file = open(self._token_file_path, "w")
        file.write(content)

    # Return boolean on validity of token
    def _token_is_outdate(self, token: str) -> bool:
        token_data = self._get_token_info(token)
        return not token_data.expires_in_seconds > 0

                ############################
                ### Interaction with API ###
                ############################

    # Return a JSON with info on the token
    #   "resource_owner_id": int
    #   "scopes": array(string)
    #   "expires_in_seconds": int
    #   "application": JSON of uid
    #       "uid": sting
    #   "created_at": int
    def _get_token_info(self, token: str) -> JsonDict:
        headers = {'Authorization': 'bearer' + token}
        response = requests.get(_FT_TOKEN_INFO_URL, headers=headers)
        return response.json()

    # Return the access token take client_id and client_secret of your 42 application
    def _get_new_token(self, client_id: str, client_secret: str) -> str:
        client = BackendApplicationClient(client_id=client_id)
        api = OAuth2Session(client=client)
        return api.fetch_token(_FT_TOKEN_URL, client_id=client_id, client_secret=client_secret)





