import os.path
import mimetypes
from typing import Tuple

def file(
    api,
    url: str,
    http_method: str,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)

def file_upload_file(
    api,
    url: str,
    http_method: str,
    local_path: str) -> Tuple[str, int]:
    with open(local_path, "rb") as fd:
        data = fd.read()
    
    mime = mimetypes.guess_type(local_path)[0]

    # Not sure whether this params are required, however they are present on cloud.mail.ru website
    params = {
        "x-email": api.client_instance.login,
        "cloud_domain": 2
    }

    response = api.client_instance.session.put(url, params=params, headers={"Content-Type": mime}, data=data)

    return response.text, int(response.request.headers["Content-Length"])

def _add(
    api,
    url: str,
    http_method: str,
    cloud_path: str,
    cloud_hash: str,
    file_size: int,
    rename_on_conflict=True) -> dict:

    data = {
        "home": cloud_path,
        "hash": cloud_hash,
        "size": file_size,
        "token": api.csrf_token,
        "api": 2,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method, data=data)

def file_add(
    api,
    url: str,
    http_method: str,
    local_path: str,
    cloud_path: str) -> dict:

    cloud_hash, file_size = api.file._upload_file(local_path)
    if cloud_path.endswith("/"):
        cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

    return _add(api, url, http_method, cloud_path, cloud_hash, file_size)

def file_remove(
    api,
    url: str,
    http_method: str,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, data=data)

def file_move(
    api,
    url: str,
    http_method: str,
    cloud_path: str,
    to_folder_path: str) -> dict:
    data = {
        "home": cloud_path,
        "folder": to_folder_path,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_rename(
    api,
    url: str,
    http_method: str,
    cloud_path: str,
    new_name: str,
    rename_on_conflict=True) -> dict:

    data = {
        "home": cloud_path,
        "name": new_name,
        "token": api.csrf_token,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method, data=data)

def file_publish(
    api,
    url: str,
    http_method: str,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_unpublish(
    api,
    url: str,
    http_method: str,
    weblink: str) -> dict:

    data = {
        "weblink": weblink,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_copy(
    api,
    url: str,
    http_method: str,
    cloud_path: str,
    to_folder_path: str,
    rename_on_conflict=True) -> dict:

    data = {
        "home": cloud_path,
        "folder": to_folder_path,
        "token": api.csrf_token,
    }
    if rename_on_conflict:
        data.update({"conflict": "rename"})

    return api(url, http_method, data=data)

def file_history(
    api,
    url: str,
    http_method: str,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)
