import json
from ApiManager import ApiManager
from datetime import datetime, timedelta
import re


class Collector:
    base_url = 'https://api.intra.42.fr/v2/'
    token = ''

    def __init__(self, access_token):
        self.token = access_token

    @staticmethod
    def get_connections_object(users: json) -> list:
        connections = []
        for user in users:
            match = re.match(r"[e]([1-3])[r](\d{1,2})[p](\d{1,2})", str(user["host"]))
            connection = {}
            if match:
                connection["floor"] = match.group(1)
                connection["rank"] = match.group(2)
                connection["station"] = match.group(3)
                connection["Id"] = user["id"]
                connection["login"] = user["user"]["login"]
                connection["host"] = user["host"]
                connection["Beginning"] = user["begin_at"]
                connection["Finish"] = user["end_at"]
                connections.append(connection)
        return connections

    @staticmethod
    def get_all_pages(api_manager: ApiManager, request):
        connections = []
        page = 0
        first = True
        while first or len(users) == 100:
            first = False
            request["params"].update({'page[number]': page})
            response = api_manager.get(request["core_request"], request["filters"], request["params"])
            # print(response)
            if response.status_code != 200:
                print(response.status_code)
                print(response.reason)
                break
            users = json.loads(response.content)
            page += 1
            connections = connections + Collector.get_connections_object(users)
        return connections

    # get new connetion in cluster from date - plage to date plage in seconds
    def get_new_connection_on_plage(self, date: datetime, plage: str) -> json:
        from_date = date - timedelta(seconds=plage)
        api_manager = ApiManager(self.token, self.base_url)
        request = {}
        request["core_request"] = 'campus/1/locations'
        request["filters"] = {'filter[active]': 'true',
                   'range[begin_at]': from_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z') + ','
                                      + date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}
        request["params"] = {'page[size]': '100'}
        return Collector.get_all_pages(api_manager, request)

    def get_active_now(self) -> json:
        api_manager = ApiManager(self.token, self.base_url)
        request = {}
        request["core_request"] = 'campus/1/locations'
        request["filters"] = {'filter[active]': 'true'}
        request["params"] = {'page[size]': '100', 'page[number]': 0}
        return Collector.get_all_pages(api_manager, request)
