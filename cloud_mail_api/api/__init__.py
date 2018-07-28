__all__ = ["API"]

import functools
import os
import json
import importlib

from requests.cookies import RequestsCookieJar

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
    def __init__(self,
        client_instance,
        api_config_path=None,
        preload_all_methods=True):

        self.client_instance = client_instance

        self._csrf_token = None
        self.config = None

        self.__is_url_cycle = False
        self.__url_parts = []

        self.load_config(api_config_path or f"{os.path.dirname(__file__)}/api_config.json")
        if preload_all_methods:
            self.preload_all_methods()

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
    def csrf_token(self) -> str:
        if self._csrf_token is None:
            response = self.tokens.csrf(True)

            if response.get("body") == "user":
                self.client_instance.auth()
                return self.csrf_token

            if not isinstance(response["body"], dict):
                raise errors.CloudMailUnexpectedTokenError(
                    f"Received wrong response format while obtaining token: 'body' must be dict, not {repr(response['body'])}")

            self._csrf_token = response["body"]["token"]
        return self._csrf_token

    def sdc(self) -> bool:
        response = self.client_instance.session.get(self.config["endpoints"]["SDC_ENDPOINT"])
        return response.status_code == 200

    def load_config(self, path: str) -> dict:
        with open(path) as file:
            self.config = json.loads(file.read())
        return self.config

    @memoize
    def load_function(self, path: str) -> dict:
        config = self.load_method_config(path)
        if config is None:
            raise NotImplementedError()

        method_module_ = config["location"]["module"]
        method_package = config["location"]["package"]
        method_function_name = config["location"]["function"]

        method_module = importlib.import_module(method_module_, method_package)

        method = getattr(method_module, method_function_name, None)
        return method

    @memoize
    def load_method_config(self, path: str) -> dict:
        return self.config["api_methods"].get(path)

    def preload_all_methods(self) -> None:
        try:
            for path in self.config["api_methods"]:
                self.load_method_config(path)
                self.load_function(path)
        except:
            return False
        else:
            return True

    def raw_api_caller(self,
        path: str,
        http_method: str,
        fullpath=True,
        **kwargs) -> dict:

        url = path if fullpath else "/".join([self.config["endpoints"]["API_BASE_ENDPOINT"], path.strip(r"\/")])

        response = getattr(self.client_instance.session, http_method.lower())(
            url, headers={"X-Requested-With": "XMLHttpRequest"}, **kwargs)

        return response.json() if "application/json" in response.headers["Content-Type"] else response

    def url_resolver(self, *method_args, **method_kwargs) -> dict:
        path = "/".join(self.__url_parts)
        self.__url_parts.clear()

        method = self.load_function(path)
        http_method = self.load_method_config(path).get("method")
        endpoint = self.load_method_config(path).get(
            "endpoint",
            self.config["endpoints"]["API_BASE_ENDPOINT"]
        )
        path = path.strip(r"\/") if not self.load_method_config(path).get("no_path") else ""
        url = "/".join([endpoint, path])

        if method is not None:
            method_result = method(self, url, http_method, *method_args, **method_kwargs)
            return method_result
        else:
            raise NotImplementedError(f"No such method with path '{path}' in implemented api")
