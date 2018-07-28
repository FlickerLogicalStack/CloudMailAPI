from typing import Iterable

def zip(
    api,
    url: str,
    http_method: str,
    cloud_paths: Iterable[str],
    name: str) -> dict:

    data = {
        "home_list": str(cloud_paths).replace("'", '"'),
        "name": name,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)
