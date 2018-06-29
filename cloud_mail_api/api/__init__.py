__all__ = ["API"]

from requests.cookies import RequestsCookieJar

from .. import constants
from .file import FileMethodsGroup
from .folder import FolderMethodsGroup
from .tokens import TokensMethodsGroup
from .trashbin import TrashbinMethodsGroup
from .single import SingleMethodsGroup
from .user import UserMethodsGroup


class API:
    def __init__(self, cloud_mail_instance):
        self.cloud_mail_instance = cloud_mail_instance

        self.register_method_group("file", FileMethodsGroup(cloud_mail_instance, self))
        self.register_method_group("folder", FolderMethodsGroup(cloud_mail_instance, self))
        self.register_method_group("tokens", TokensMethodsGroup(cloud_mail_instance, self))
        self.register_method_group("trashbin", TrashbinMethodsGroup(cloud_mail_instance, self))
        self.register_method_group("user", UserMethodsGroup(cloud_mail_instance, self))
        
        self.single_methods_group = SingleMethodsGroup(cloud_mail_instance, self)

    def register_method_group(self, name, methods_group):
        if name not in self.__dict__:
            setattr(self, name, methods_group)

    def __getattr__(self, name):
        if name not in vars(self):
            if name in dir(self.single_methods_group):
                return getattr(self.single_methods_group, name)
        return super().__getattribute__(name)

    @property
    def session(self) -> RequestsCookieJar:
        return self.cloud_mail_instance.session

    @property
    def csrf_token(self) -> str:
        return self.cloud_mail_instance.csrf_token

    def sdc(self):
        response = self.cloud_mail_instance.session.get(constants.SDC_ENDPOINT)
        return response.status_code == 200

    def __call__(self, path: str, http_method: str, fullpath=False, **kwargs) -> dict:
        if fullpath:
            url = path
        else:
            url = "/".join([constants.API_BASE_ENDPOINT, path.strip(r"\/")])

        print(url)
        response = getattr(self.session, http_method.lower())(
            url, headers={"X-Requested-With": "XMLHttpRequest"}, **kwargs)

        return response.json()
