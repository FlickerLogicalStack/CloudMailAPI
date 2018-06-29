__all__ = ["TokensMethodsGroup"]

import os.path

from .. import constants
from .. import errors

class TokensMethodsGroup:
    __slots__ = ["cloud_mail_instance", "api"]
    def __init__(self, cloud_mail_instance, api_instance):
        self.cloud_mail_instance = cloud_mail_instance
        self.api = api_instance

    def csrf(self, resolve_nosdc=False) -> dict:
        url = constants.API_TOKENS_CSRF_PATH

        response = self.api(url, "post")

        if (response.get("status") == 403) and (response.get("body") == "nosdc") and (resolve_nosdc):
            sdc_response = self.api.sdc()
            if sdc_response:
                return self.csrf()
            else:
                raise errors.CloudMailSdcGettingError(f"Received unexpected status code: {sdc_response.status_code}")
        else:
            return response

    def download(self) -> dict:
        url = constants.API_TOKENS_DOWNLOAD_PATH

        data = {
            "token": self.csrf(True)["body"]["token"]
        }

        return self.api(url, "post", data=data)
