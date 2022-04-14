import requests

class ApiManager:
    def __init__(self, token: str, base_url: str):
        self.token = token
        if base_url.endswith('/'):
            base_url = base_url.removesuffix('/')
        self.base_url = base_url

    def get(self, core_request: str, filters: dict, params: dict, headers: dict = {}):
        headers.update({'Authorization': 'bearer ' + self.token})
        params.update(filters)
        return requests.get(self.base_url + core_request, params=params, headers=headers)
