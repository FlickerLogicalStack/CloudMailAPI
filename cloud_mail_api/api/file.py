import os.path
from typing import Tuple

from .. import constants

def file(api, http_method, cloud_path: str) -> dict:
    url = constants.API_FILE_PATH

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method: str, params=data)

def file_upload_file(api, http_method, local_path: str) -> Tuple[str, int]:
    files = {
        "file": (
            os.path.basename(local_path),
            open(local_path, "rb"),
            "application/octet-stream"
        )
    }

    response = api.cloud_mail_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)
    if response.status_code == 403:
        response = api.cloud_mail_instance.session.put(constants.API_FILE_UPLOAD_ENDPOINT, files=files)
    return response.text, int(response.request.headers["Content-Length"])

def _add(api, http_method, cloud_path: str, cloud_hash: str, file_size: int, rename_on_conflict=True) -> dict:
    url = constants.API_FILE_ADD_PATH

    data = {
        "home": cloud_path,
        "hash": cloud_hash,
        "size": file_size,
        "token": api.csrf_token,
        "api": 2,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method: str, data=data)

def file_add(api, http_method, local_path: str, cloud_path: str) -> dict:
    cloud_hash, file_size = file_upload_file(api, http_method, local_path)
    if cloud_path.endswith("/"):
        cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

    return _add(api, http_method, cloud_path, cloud_hash, file_size)

def file_remove(api, http_method, cloud_path: str) -> dict:
    url = constants.API_FILE_REMOVE_PATH

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method: str, data=data)

def file_move(api, http_method, cloud_path: str, to_folder_path: str) -> dict:
    url = constants.API_FILE_MOVE_PATH

    data = {
        "home": cloud_path,
        "folder": to_folder_path,
        "token": api.csrf_token
    }

    return api(url, http_method: str, data=data)

def file_rename(api, http_method, cloud_path: str, new_name: str, rename_on_conflict=True) -> dict:
    url = constants.API_FILE_RENAME_PATH

    data = {
        "home": cloud_path,
        "name": new_name,
        "token": api.csrf_token,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method: str, data=data)

def file_publish(api, http_method, cloud_path: str) -> dict:
    url = constants.API_FILE_PUBLISH_PATH

    data = {
        "home": cloud_path,
        "token": api.csrf_token
    }

    return api(url, http_method: str, data=data)

def file_unpublish(api, http_method, web_link: str) -> dict:
    url = constants.API_FILE_UNPUBLISH_PATH

    data = {
        "weblink": web_link,
        "token": api.csrf_token
    }

    return api(url, http_method: str, data=data)

def file_copy(api, http_method, cloud_path: str, to_folder_path: str, rename_on_conflict=True) -> dict:
    url = constants.API_FILE_COPY_PATH

    data = {
        "home": cloud_path,
        "folder": to_folder_path,
        "token": api.csrf_token,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method: str, data=data)

def file_history(api, http_method, cloud_path: str) -> dict:
    url = constants.API_FILE_HISTORY_PATH

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method: str, params=data)
