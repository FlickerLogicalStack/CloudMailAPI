__all__ = ["FolderMethodsGroup"]

import os.path
from .. import constants

class FolderMethodsGroup:
    __slots__ = ["mail_cloud_instance", "api"]
    def __init__(self, mail_cloud_instance, api_instance):
        self.mail_cloud_instance = mail_cloud_instance
        self.api = api_instance

    def add(self, cloud_path: str) -> dict:
        url = constants.API_FOLDER_ADD_PATH

        data = {
            "home": cloud_path,
            "conflict": "rename",
            "token": self.mail_cloud_instance.csrf_token
        }

        return self.api(url, "post", **data)
