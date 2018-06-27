import json
import os.path
import re

import requests


class API:
    BASE_ENDPOINT = "https://cloud.mail.ru/api/v2"
    FILE_UPLOAD_ENDPOINT = "https://cloclo21-upload.cloud.mail.ru/upload/"

    def __init__(self, mail_cloud_instance):
        self.mail_cloud_instance = mail_cloud_instance

    @property
    def session(self):
        return self.mail_cloud_instance.session

    @property
    def csrf_token(self):
        return self.mail_cloud_instance.csrf_token

    def __call__(self, path, http_method, **kwargs):
        response = getattr(self.session, http_method.lower())(
            "/".join([API.BASE_ENDPOINT, path.strip(r"\/")]),
            data=kwargs, headers={"X-Requested-With": "XMLHttpRequest"})

        return response.json()

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
            response = self.session.post(DF_AUTH_ENDPOINT,
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
