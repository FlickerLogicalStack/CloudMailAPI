__all__ = ["FileMethodsGroup"]

import os.path
from typing import Tuple

from .. import constants

class FileMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api","_upload_file_url"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

        self._upload_file_url = None

    def _upload_file(self, file_path: str) -> Tuple[str, int]:
        files = {
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/octet-stream"
            )
        }

        response = self.cloud_mail_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)
        if response.status_code == 403:
            response = self.cloud_mail_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)
        return response.text, int(response.request.headers["Content-Length"])

    def _add(self, cloud_path: str, cloud_hash: str, file_size: int) -> dict:
        url = constants.API_FILE_ADD_PATH

        data = {
            "home": cloud_path,
            "hash": cloud_hash,
            "size": file_size,
            "token": self.cloud_mail_instance.csrf_token,
            "conflict": "rename",
            "api": 2,
        }

        return self.api(url, "post", data=data)

    def add(self, local_path: str, cloud_path: str) -> dict:
        cloud_hash, file_size = self._upload_file(local_path)
        if cloud_path.endswith("/"):
            cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

        return self._add(cloud_path, cloud_hash, file_size)

    def remove(self, cloud_path: str) -> dict:
        url = constants.API_FILE_REMOVE_PATH

        data = {
            "home": cloud_path,
            "token": self.cloud_mail_instance.csrf_token,
        }

        return self.api(url, "post", data=data)

    def move(self, from_file_path: str, to_folder_path: str) -> dict:
        url = constants.API_FILE_MOVE_PATH

        data = {
            "home": from_file_path,
            "folder": to_folder_path,
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", data=data)

    def rename(self, cloud_path: str, new_name: str) -> dict:
        url = constants.API_FILE_RENAME_PATH

        data = {
            "home": cloud_path,
            "name": new_name,
            "token": self.cloud_mail_instance.csrf_token,
            "conflict": "rename"
        }

        return self.api(url, "post", data=data)

    def publish(self, cloud_path: str):
        url = constants.API_FILE_PUBLISH_PATH

        data = {
            "home": cloud_path,
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", data=data)

    def unpublish(self, web_link: str):
        url = constants.API_FILE_UNPUBLISH_PATH

        data = {
            "weblink": web_link,
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", data=data)

    def copy(self, cloud_path: str, to_folder_path: str) -> dict:
        url = constants.API_FILE_COPY_PATH

        data = {
            "home": cloud_path,
            "folder": to_folder_path,
            "token": self.cloud_mail_instance.csrf_token,
            "conflict": "rename"
        }

        return self.api(url, "post", data=data)
