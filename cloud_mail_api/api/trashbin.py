from .. import constants

def trashbin(api, http_method, cloud_trashbin_path="/", limit=100) -> dict:
    url = constants.API_TRASHBIN_PATH

    data = {
        "home": cloud_trashbin_path,
        "limit": limit,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)

def trashbin_restore(api, http_method, restore_revision: int, cloud_path: str) -> dict:
    url = constants.API_TRASHBIN_RESTORE_PATH

    data = {
        "restore_revision": restore_revision,
        "path": cloud_path,
        "token": api.csrf_token,   
        "conflict": "rename"
    }

    return api(url, http_method, data=data)

def trashbin_empty(api, http_method) -> dict:
    url = constants.API_TRASHBIN_EMPTY_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)
