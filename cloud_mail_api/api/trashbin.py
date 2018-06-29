__all__ = ["TrashbinMethodsGroup"]

import os.path

from .. import constants
from .. import errors

class TrashbinMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def __call__(self, cloud_trashbin_path="/", limit=100):
        url = constants.API_TRASHBIN_PATH

        data = {
            "home": cloud_trashbin_path,
            "limit": limit,
            "token": self.cloud_mail_instance.csrf_token,
        }

        return self(url, "get", params=data)

    def restore(self, restore_revision: int, cloud_path: str):
        url = constants.API_TRASHBIN_RESTORE_PATH

        data = {
            "restore_revision": restore_revision,
            "path": cloud_path,
            "token": self.cloud_mail_instance.csrf_token,   
            "conflict": "rename"
        }

        return self.api(url, "post", data=data)

    def empty(self):
        url = constants.API_TRASHBIN_EMPTY_PATH

        data = {
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", data=data)
