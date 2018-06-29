__all__ = ["SingleMethodsGroup"]

import os.path
from typing import Iterable

from .. import constants
from .. import errors

class SingleMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def zip(self, cloud_paths: Iterable[str], name: str) -> dict:
        url = constants.API_ZIP_PATH

        data = {
            "home_list": str(cloud_paths).replace("'", '"'),
            "name": name,
            "token": self.api.csrf_token
        }

        return self.api(url, "post", data=data)

    def dispatcher(self):
        url = constants.API_DISPATCHER_PATH

        data = {
            "token": self.api.csrf_token
        }

        return self.api(url, "get", params=data)
