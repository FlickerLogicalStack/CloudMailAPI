__all__ = ["API"]

from requests.cookies import RequestsCookieJar

from .. import constants
from .file import FileMethodsGroup
from .folder import FolderMethodsGroup


class API:
    def __init__(self, mail_cloud_instance):
        self.mail_cloud_instance = mail_cloud_instance

        self.file = FileMethodsGroup(mail_cloud_instance, self)
        self.folder = FolderMethodsGroup(mail_cloud_instance, self)

    @property
    def session(self) -> RequestsCookieJar:
        return self.mail_cloud_instance.session

    @property
    def csrf_token(self) -> str:
        return self.mail_cloud_instance.csrf_token

    def __call__(self, path: str, http_method: str, fullpath=False, **kwargs) -> dict:
        if fullpath:
            url = path
        else:
            url = "/".join([constants.API_BASE_ENDPOINT, path.strip(r"\/")])

        response = getattr(self.session, http_method.lower())(
            url, data=kwargs, headers={"X-Requested-With": "XMLHttpRequest"})

        return response.json()
