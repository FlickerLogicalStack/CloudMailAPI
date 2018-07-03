__all__ = ["API"]

import functools
import os
import json
import importlib

from requests.cookies import RequestsCookieJar

from .. import constants
from .. import errors

def memoize(f):
    cache = {}
    functools.wraps(f)
    def decorate(*args, **kwargs):
        key = (tuple(args), hash(tuple(sorted(kwargs.items()))))
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]
    return decorate

class API:
    def __init__(self, cloud_mail_instance, api_config_path=None):
        self.cloud_mail_instance = cloud_mail_instance

        self._csrf_token = None

        self.__is_url_cycle = False
        self.__url_parts = []

        self.load_config(api_config_path or f"{os.path.dirname(__file__)}/api_config.json")

    def __getattr__(self, name: str):
        if (not self.__is_url_cycle) and (name in dir(self)):
            return self.__getattribute__(name)

        self.__is_url_cycle = True
        self.__url_parts.append(name)
        return self

    def __call__(self, *args, **kwargs) -> dict:
        if self.__is_url_cycle:
            self.__is_url_cycle = False
            return self.url_resolver(*args, **kwargs)
        else:
            return self.raw_api_caller(*args, **kwargs)

    @property
    def session(self) -> RequestsCookieJar:
        return self.cloud_mail_instance.session

    @property
    def csrf_token(self) -> str:
        if self._csrf_token is None:
            response = self.tokens.csrf(True)

            if response.get("body") == "user":
                self.cloud_mail_instance.auth()
                return self.csrf_token

            if not isinstance(response["body"], dict):
                raise errors.CloudMailUnexpectedTokenError(
                    f"Received wrong response format while obtaining token: 'body' must be dict, not {repr(response['body'])}")

            self._csrf_token = response["body"]["token"]
        return self._csrf_token

    def sdc(self) -> bool:
        response = self.cloud_mail_instance.session.get(constants.SDC_ENDPOINT)
        return response.status_code == 200

    def load_config(self, path: str) -> dict:
        with open(path) as file:
            self.config = json.loads(file.read())
        return self.config

    @memoize
    def load_function(self, url: str) -> dict:
        try:
            config = self.load_method_config(url)
            if config is None:
                raise NotImplementedError()

            method_module_ = config["location"]["module"]
            method_package = config["location"]["package"]
            method_function_name = config["location"]["function"]

            method_module = importlib.import_module(method_module_, method_package)

            method = getattr(method_module, method_function_name, None)
            return method
        except:
            return None

    @memoize
    def load_method_config(self, url: str) -> dict:
        return self.config["api_methods"].get(url)

    def raw_api_caller(self, path: str, http_method: str, fullpath=False, **kwargs) -> dict:
        url = path if fullpath else "/".join([constants.API_BASE_ENDPOINT, path.strip(r"\/")])

        response = getattr(self.session, http_method.lower())(
            url, headers={"X-Requested-With": "XMLHttpRequest"}, **kwargs)

        return response.json() if "application/json" in response.headers["Content-Type"] else response

    def url_resolver(self, *method_args, **method_kwargs) -> dict:
        url = "/".join(self.__url_parts)
        self.__url_parts.clear()

        method = self.load_function(url)
        http_method = self.load_method_config(url).get("method")

        if method is not None:
            method_result = method(self, http_method, *method_args, **method_kwargs)
            return method_result
        else:
            raise NotImplementedError("No such method with path '{url}' in implemented api")
