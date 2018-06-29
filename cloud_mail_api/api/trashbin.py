from .. import constants

def trashbin(api, cloud_trashbin_path="/", limit=100) -> dict:
    url = constants.API_TRASHBIN_PATH

    data = {
        "home": cloud_trashbin_path,
        "limit": limit,
        "token": api.csrf_token,
    }

    return api(url, "get", params=data)

def trashbin_restore(api, restore_revision: int, cloud_path: str) -> dict:
    url = constants.API_TRASHBIN_RESTORE_PATH

    data = {
        "restore_revision": restore_revision,
        "path": cloud_path,
        "token": api.csrf_token,   
        "conflict": "rename"
    }

    return api(url, "post", data=data)

def trashbin_empty(api) -> dict:
    url = constants.API_TRASHBIN_EMPTY_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, "post", data=data)
