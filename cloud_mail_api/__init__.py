import json
import os.path
import re
import sys

import requests
from requests.cookies import RequestsCookieJar

from . import api
from . import errors


class CloudMail:
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

        self.session = requests.Session()
        self.api = api.API(self)

    def is_cookies_valid(self) -> bool:
        return self.api.tokens.csrf(True)["body"] != "user"

    def load_csrf(self) -> bool:
        """
        Download csrf-token from mail.ru server and put it in session
        """

        resp = self.api.tokens.csrf(True)

        if isinstance(resp["body"], dict):
            self.session.headers["X-CSRF-Token"] = resp["body"]["token"]
            return True

        return False

    def auth(self) -> bool:
        response = self.session.post(
            self.api.config["endpoints"]["MAILRU_AUTH_ENDPOINT"],
            params={"Login": self.login, "Password": self.password}
        )

        if ("fail=1" in response.url) and ("https://e.mail.ru/login" in response.url):
            raise errors.CloudMailWrongAuthData("Wrong login/password data.")

        if response.url == self.api.config["endpoints"]["TWO_FACTOR_AUTH_ENDPOINT"]:
            self.session.post(
                self.api.config["endpoints"]["TWO_FACTOR_AUTH_ENDPOINT"],
                data={
                    "csrf": re.findall(r'"csrf":"(.+)","device"', response.text)[0],
                    "Login": self.login,
                    "AuthCode": int(input("Enter AuthCode: ")),
                    "Permanent": "1"
                }
            )

        self.load_csrf()

        return self.is_cookies_valid()


    def save_cookies_to_file(self, file_path="cookies.json") -> RequestsCookieJar:
        with open(file_path, "w") as file:
            json.dump(
                requests.utils.dict_from_cookiejar(self.session.cookies), file, indent=4
            )
        return self.session.cookies


    def load_cookies_from_file(self, file_path="cookies.json") -> RequestsCookieJar:
        with open(file_path, "r") as file:
            self.session.cookies = requests.utils.cookiejar_from_dict(json.load(file))

        return self.session.cookies


    def update_cookies_from_dict(self, dict_={}, **kwargs) -> RequestsCookieJar:
        dict_.update(kwargs)
        for k, v in dict_.items():
            self.session.cookies[k] = v

        return self.session.cookies
