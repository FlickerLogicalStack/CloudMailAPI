__all__ = ["BillingMethodsGroup"]

import os.path

from .. import constants
from .. import errors

class BillingMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def rates(self):
        url = constants.API_BILLING_RATES_PATH

        data = {
            "token": self.api.csrf_token,
        }

        return self.api(url, "get", params=data)
