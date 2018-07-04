import os.path
from typing import Tuple

def file(
    api,
    url,
    http_method,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)

def file_upload_file(
    api,
    url,
    http_method,
    local_path: str) -> Tuple[str, int]:

    files = {
        "file": (
            os.path.basename(local_path),
            open(local_path, "rb"),
            "application/octet-stream"
        )
    }

    response = api.cloud_mail_instance.session.put(url, files=files)
    if response.status_code == 403:
        response = api.cloud_mail_instance.session.put(url, files=files)
    return response.text, int(response.request.headers["Content-Length"])

def _add(
    api,
    url,
    http_method,
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
    url,
    http_method,
    local_path: str,
    cloud_path: str) -> dict:

    cloud_hash, file_size = api.file._upload_file(local_path)
    if cloud_path.endswith("/"):
        cloud_path = os.path.join(cloud_path, os.path.basename(local_path))

    return _add(api, url, http_method, cloud_path, cloud_hash, file_size)

def file_remove(
    api,
    url,
    http_method,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, data=data)

def file_move(
    api,
    url,
    http_method,
    cloud_path:
    str,
    to_folder_path: str) -> dict:
    data = {
        "home": cloud_path,
        "folder": to_folder_path,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_rename(
    api,
    url,
    http_method,
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
    url,
    http_method,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_unpublish(
    api,
    url,
    http_method,
    weblink: str) -> dict:

    data = {
        "weblink": web_link,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def file_copy(
    api,
    url,
    http_method,
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
    url,
    http_method,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)
