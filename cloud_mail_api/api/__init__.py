__all__ = ["API"]

from requests.cookies import RequestsCookieJar

from .. import constants
from .file import FileMethodsGroup
from .folder import FolderMethodsGroup


class API:
    __slots__ = ["cloud_mail_instance", "file", "folder"]
    def __init__(self, cloud_mail_instance):
        self.cloud_mail_instance = cloud_mail_instance

        self.file = FileMethodsGroup(cloud_mail_instance, self)
        self.folder = FolderMethodsGroup(cloud_mail_instance, self)

    @property
    def session(self) -> RequestsCookieJar:
        return self.cloud_mail_instance.session

    @property
    def csrf_token(self) -> str:
        return self.cloud_mail_instance.csrf_token

    def __call__(self, path: str, http_method: str, fullpath=False, **kwargs) -> dict:
        if fullpath:
            url = path
        else:
            url = "/".join([constants.API_BASE_ENDPOINT, path.strip(r"\/")])

        print(url)
        response = getattr(self.session, http_method.lower())(
            url, headers={"X-Requested-With": "XMLHttpRequest"}, **kwargs)

        return response.json()
