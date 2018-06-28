__all__ = ["FolderMethodsGroup"]

import os.path
from .. import constants

class FolderMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def add(self, cloud_path: str) -> dict:
        url = constants.API_FOLDER_ADD_PATH

        data = {
            "home": cloud_path,
            "conflict": "rename",
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", data=data)

    def remove(self, cloud_path: str) -> dict:
        url = constants.API_FOLDER_REMOVE_PATH

        data = {
            "home": cloud_path,
            "token": self.cloud_mail_instance.csrf_token,
            "api": 2,
            "email": self.cloud_mail_instance.login,
            "x-email": self.cloud_mail_instance.login,
        }

        return self.api(url, "post", data=data)

    def move(self, folder_path: str, to_folder_path: str):
        url = constants.API_FOLDER_MOVE_PATH

        data = {
            "home": folder_path,
            "folder": to_folder_path,
            "token": self.cloud_mail_instance.csrf_token,
            "api": 2,
            "email": self.cloud_mail_instance.login,
            "x-email": self.cloud_mail_instance.login,
        }

        return self.api(url, "post", data=data)

    def rename(self, cloud_path: str, new_name: str):
        url = constants.API_FOLDER_RENAME_PATH

        data = {
            "home": cloud_path,
            "name": new_name,
            "token": self.cloud_mail_instance.csrf_token,
            "conflict": "rename",
            "api": 2,
            "email": self.cloud_mail_instance.login,
            "x-email": self.cloud_mail_instance.login,
        }

        return self.api(url, "post", data=data)

    def publish(self, cloud_path: str):
        url = constants.API_FOLDER_PUBLISH_PATH

        data = {
            "home": folder_path,
            "folder": to_folder_path,
            "token": self.cloud_mail_instance.csrf_token,
            "api": 2,
            "email": self.cloud_mail_instance.login,
            "x-email": self.cloud_mail_instance.login,
        }

        return self.api(url, "post", data=data)