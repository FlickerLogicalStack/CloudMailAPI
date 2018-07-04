from typing import Iterable

def zip(
    api,
    url,
    http_method,
    cloud_paths: Iterable[str],
    name: str) -> dict:

    data = {
        "home_list": str(cloud_paths).replace("'", '"'),
        "name": name,
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)
