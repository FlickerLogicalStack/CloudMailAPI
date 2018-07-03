from typing import Iterable

from .. import constants

def zip(api, http_method, cloud_paths: Iterable[str], name: str) -> dict:
    url = constants.API_ZIP_PATH

    data = {
        "home_list": str(cloud_paths).replace("'", '"'),
        "name": name,
        "token": api.csrf_token
    }

    return api(url, http_method: str, data=data)

def dispatcher(api, http_method) -> dict:
    url = constants.API_DISPATCHER_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method: str, params=data)
