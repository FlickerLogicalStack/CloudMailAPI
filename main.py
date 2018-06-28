import json
import os.path
import re

import requests

from api import API

class MailCloud:
    CSRF_TOKEN_ENDPOINT = "https://cloud.mail.ru/api/v2/tokens/csrf"
    MAILRU_AUTH_ENDPOINT = "https://auth.mail.ru/cgi-bin/auth"
    SDC_ENDPOINT = "https://auth.mail.ru/sdc?from=https://cloud.mail.ru/home"
    DF_AUTH_ENDPOINT = "https://auth.mail.ru/cgi-bin/secstep"

    def __init__(self, login, password):
        self.login = login
        self.password = password

        self._csrf_token = None

        self.session = requests.Session()
        self.api = API(self)

    @property
    def csrf_token(self):
        if self._csrf_token is None:
            response = self.session.post(MailCloud.CSRF_TOKEN_ENDPOINT).json()

            if response.get("body") == "user":
                self.auth()
                self.session.get(MailCloud.SDC_ENDPOINT)
                response = self.session.post(MailCloud.CSRF_TOKEN_ENDPOINT).json()

            elif response.get("body") == "nosdc":
                self.session.get(MailCloud.SDC_ENDPOINT)
                response = self.session.post(MailCloud.CSRF_TOKEN_ENDPOINT).json()
            
            self._csrf_token = response["body"]["token"]
        return self._csrf_token

    def auth(self):
        response = self.session.post(MailCloud.MAILRU_AUTH_ENDPOINT,
            params={"Login": self.login, "Password": self.password}
        )
        if response.url == MailCloud.DF_AUTH_ENDPOINT:
            response = self.session.post(MailCloud.DF_AUTH_ENDPOINT,
                data={
                    "csrf": re.findall(r'"csrf":"(.+)","device"', response.text)[0],
                    "Login": self.login,
                    "AuthCode": int(input("Enter AuthCode: ")),
                    "Permanent": "1"
                }
            )

        self.session.get(MailCloud.SDC_ENDPOINT)

    def save_cookies_to_file(self, file_path):
        with open(file_path, "w") as file:
            json.dump(
                requests.utils.dict_from_cookiejar(self.session.cookies), file, indent=4
            )

    def load_cookies_from_file(self, file_path):
        with open(file_path, "r") as file:
            self.session.cookies = requests.utils.cookiejar_from_dict(json.load(file))
    
    def update_cookies_from_dict(self, dict_={}, **kwargs):
        dict_.update(kwargs)
        for k, v in dict_.items():
            self.session.cookies[k] = v
