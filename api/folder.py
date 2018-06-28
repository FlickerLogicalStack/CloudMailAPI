__all__ = ["FolderMethodsGroup"]

import os.path
from .. import constants

class FolderMethodsGroup:
    def __init__(self, mail_cloud_instance, api_instance):
        self.mail_cloud_instance = mail_cloud_instance
        self.api_instance = api_instance

    def add(self, cloud_path):
        url = constants.API_FOLDER_ADD

        data = {
            "home": cloud_path,
            "conflict": "rename",
            "token": self.mail_cloud_instance.csrf_token
        }

        response = self.mail_cloud_instance.session.post(url, data=data, headers={"X-Requested-With": "XMLHttpRequest"})

        return response.json()
