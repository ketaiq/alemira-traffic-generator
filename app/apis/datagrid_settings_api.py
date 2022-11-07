from app.apis.user_api_endpoint import UserAPIEndPoint
from app.models.user import User
import requests
from app.utils.string import request_http_error_msg, request_timeout_msg


class DatagridSettingsAPI(UserAPIEndPoint):
    def __init__(
        self,
        client=None,
    ):
        super().__init__(client)
        self.url = self.uri + "datagrid-settings/"

    def get_datagrid_tenants(self, headers: dict) -> dict:
        if self.client is None:
            r = requests.get(self.url + "datagrid-tenants", headers=headers)
            r.raise_for_status()
            return r.json()
        with self.client.get(
            self.url + "datagrid-tenants",
            headers=headers,
            name="get datagrid tenants",
            catch_response=True,
        ) as response:
            if response.ok:
                return response.json()
            elif response.elapsed.total_seconds() > self.TIMEOUT_MAX:
                response.failure(request_timeout_msg())
            else:
                response.failure(request_http_error_msg(response))
