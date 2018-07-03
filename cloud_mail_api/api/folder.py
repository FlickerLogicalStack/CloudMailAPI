from .. import constants

def folder(api, http_method, cloud_path: str, limit=100, offset=0, sort={"type":"name","order":"asc"}) -> dict:
    url = constants.API_FOLDER_PATH

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
        "limit": limit,
        "offset": offset,
        "sort": sort,
    }

    return api(url, http_method: str, params=data)

def folder_add(api, http_method, cloud_path: str) -> dict:
    url = constants.API_FOLDER_ADD_PATH

    data = {
        "home": cloud_path,
        "conflict": "rename",
        "token": api.csrf_token
    }

    return api(url, http_method: str, data=data)
