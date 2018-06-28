__all__ = ["FileMethodsGroup"]

import os.path
from typing import Tuple

from .. import constants

class FileMethodsGroup:
    __slots__ = ["mail_cloud_instance", "api"]
    def __init__(self, mail_cloud_instance, api_instance):
        self.mail_cloud_instance = mail_cloud_instance
        self.api = api_instance

    def _upload_file(self, file_path: str) -> Tuple[str, int]:
        files = {
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/octet-stream"
            )
        }

        response = self.mail_cloud_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)

        return response.text, int(response.request.headers["Content-Length"])

    def _add(self, cloud_path: str, cloud_hash: str, file_size: int) -> dict:
        url = constants.API_FILE_ADD_PATH

        data = {
            "home": cloud_path,
            "hash": cloud_hash,
            "conflict": "rename",
            "size": file_size,
            "api": 2,
            "token": self.mail_cloud_instance.csrf_token
        }

        return self.api(url, "post", **data)

    def add(self, local_path: str, cloud_path: str) -> dict:
        cloud_hash, file_size = self._upload_file(local_path)
        if cloud_path.endswith("/"):
            cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

        return self._add(cloud_path, cloud_hash, file_size)
