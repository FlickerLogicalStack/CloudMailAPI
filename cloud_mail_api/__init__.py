import json
import os.path
import re
import sys

import requests
from requests.cookies import RequestsCookieJar

from . import api
from . import constants
from . import errors



class CloudMail:
    __slots__ = ["login", "password", "_csrf_token", "session", "api"]
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

        self._csrf_token = None

        self.session = requests.Session()
        self.api = api.API(self)


    # TODO: Rewrite with self.api.tokens.csrf()
    @property
    def csrf_token(self) -> str:
        if self._csrf_token is None:
            response = self.session.post(constants.CSRF_TOKEN_ENDPOINT).json()

            if response.get("body") == "user":
                self.auth()
                return self.csrf_token

            elif response.get("body") == "nosdc":
                self.session.get(constants.SDC_ENDPOINT)
                return self.csrf_token
            
            if not isinstance(response["body"], dict):
                raise errors.CloudMailUnexpectedTokenError(
                    f"Received wrong response format while obtaining token: 'body' must be dict, not {repr(response['body'])}")

            self._csrf_token = response["body"]["token"]
        return self._csrf_token


    def auth(self) -> bool:
        response = self.session.post(constants.MAILRU_AUTH_ENDPOINT,
            params={"Login": self.login, "Password": self.password}
        )

        if ("fail=1" in response.url) and ("https://e.mail.ru/login" in response.url):
            raise errors.CloudMailWrongAuthData("Wrong login/password data.")

        if response.url == constants.DF_AUTH_ENDPOINT:
            self.session.post(constants.DF_AUTH_ENDPOINT,
                data={
                    "csrf": re.findall(r'"csrf":"(.+)","device"', response.text)[0],
                    "Login": self.login,
                    "AuthCode": int(input("Enter AuthCode: ")),
                    "Permanent": "1"
                }
            )

        return True


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
