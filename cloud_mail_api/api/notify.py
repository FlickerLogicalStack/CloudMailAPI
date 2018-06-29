__all__ = ["NotifyMethodsGroup"]

import os.path

from .. import constants
from .. import errors

class NotifyMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def applink(self, phone_number: str):
        url = constants.API_APPLINK_PATH

        data = {
            "phone": phone_number,
            "token": self.cloud_mail_instance.csrf_token
        }

        return self.api(url, "post", json=data)
