__all__ = ["API"]

from .file import FileMethodsGroup
from .folder import FolderMethodsGroup
from .. import constants

class API:
    def __init__(self, mail_cloud_instance):
        self.mail_cloud_instance = mail_cloud_instance

        self.file = FileMethodsGroup(mail_cloud_instance, self)
        self.folder = FolderMethodsGroup(mail_cloud_instance, self)

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