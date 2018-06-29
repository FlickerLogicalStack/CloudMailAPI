from typing import Iterable

from .. import constants

def zip(api, cloud_paths: Iterable[str], name: str) -> dict:
    url = constants.API_ZIP_PATH

    data = {
        "home_list": str(cloud_paths).replace("'", '"'),
        "name": name,
        "token": api.csrf_token
    }

    return api(url, "post", data=data)

def dispatcher(api) -> dict:
    url = constants.API_DISPATCHER_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, "get", params=data)
