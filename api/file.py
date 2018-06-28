__all__ = ["FileMethodsGroup"]

import os.path
from .. import constants

class FileMethodsGroup:
    def __init__(self, mail_cloud_instance, api_instance):
        self.mail_cloud_instance = mail_cloud_instance
        self.api_instance = api_instance

    def _upload_file(self, file_path):
        files = {
            "file": (
                os.path.basename(file_path),
                open(file_path, "rb"),
                "application/octet-stream"
            )
        }

        response = self.mail_cloud_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)

        return response.text, response.request.headers["Content-Length"]

    def _add(self, cloud_path, cloud_hash, file_size, api=2, conflict="rename"):
        url = constants.API_FILE_ADD

        data = {
            "home": cloud_path,
            "hash": cloud_hash,
            "conflict": conflict,
            "size": file_size,
            "api": api,
            "token": self.mail_cloud_instance.csrf_token
        }

        response = self.mail_cloud_instance.session.post(url, data=data, headers={"X-Requested-With": "XMLHttpRequest"})

        return response.json()

    def add(self, local_path, cloud_path):
        cloud_hash, file_size = self._upload_file(local_path)
        if cloud_path.endswith("/"):
            cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

        return self._add(cloud_path, cloud_hash, file_size)