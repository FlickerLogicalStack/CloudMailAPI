__all__ = ["API"]

from requests.cookies import RequestsCookieJar

from .. import constants
from .. import errors

from . import billing
from . import file
from . import folder
from . import notify
from . import single
from . import tokens
from . import trashbin
from . import user


class MethodsStore:
    def __init__(self):
        self.links = {
            "tokens/csrf": tokens.tokens_csrf,
            "tokens/download": tokens.tokens_download,
            
            "trashbin": trashbin.trashbin,
            "trashbin/restore": trashbin.trashbin_restore,
            "trashbin/empty": trashbin.trashbin_empty,
            
            "user": user.user,
            "user/space": user.user_space,
            
            "billing/rates": billing.billing_rates,
            
            "zip": single.zip,
            "dispatcher": single.dispatcher,
            "notify/applink": notify.notify_applink,

            "folder": folder.folder,
            "folder/add": folder.folder_add,
            "folder/move": file.file_move,
            "folder/remove": file.file_remove,
            "folder/rename": file.file_rename,
            "folder/copy": file.file_copy,
            "folder/publish": file.file_publish,
            "folder/unpublish": file.file_unpublish,

            "file": file.file,
            "file/add": file.file_add,
            "file/_uload_file": file.file_upload_file,
            "file/move": file.file_move,
            "file/remove": file.file_remove,
            "file/rename": file.file_rename,
            "file/copy": file.file_copy,
            "file/publish": file.file_publish,
            "file/unpublish": file.file_unpublish,
        }

    def get_method(self, url):
        return self.links.get(url)


class API:
    def __init__(self, cloud_mail_instance):
        self.cloud_mail_instance = cloud_mail_instance

        self._csrf_token = None

        self.__is_url_cycle = False
        self.__url_parts = []
        self.methods_store = MethodsStore()

    def __getattr__(self, name):
        if self.__is_url_cycle:
            self.__url_parts.append(name)
            return self
        else:
            if name not in dir(self):
                self.__is_url_cycle = True
            return getattr(self, name)

    def __call__(self, *args, **kwargs) -> dict:
        if self.__is_url_cycle:
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

    def raw_api_caller(self, path: str, http_method: str, fullpath=False, **kwargs) -> dict:
        if fullpath:
            url = path
        else:
            url = "/".join([constants.API_BASE_ENDPOINT, path.strip(r"\/")])

        print(url)
        response = getattr(self.session, http_method.lower())(
            url, headers={"X-Requested-With": "XMLHttpRequest"}, **kwargs)

        return response.json()

    def url_resolver(self, *args, **kwargs) -> dict:
        url = "/".join(self.__url_parts)
        self.__url_parts.clear()
        self.__is_url_cycle = False

        method = self.methods_store.get_method(url)
        if method is not None:
            return method(self, *args, **kwargs)
        else:
            raise NotImplementedError("No such method in implemented api")
