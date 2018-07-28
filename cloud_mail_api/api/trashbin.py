def trashbin(
    api,
    url: str,
    http_method: str,
    cloud_trashbin_path="/",
    limit=100) -> dict:

    data = {
        "home": cloud_trashbin_path,
        "limit": limit,
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)

def trashbin_restore(
    api,
    url: str,
    http_method: str,
    restore_revision: int,
    cloud_path: str) -> dict:

    data = {
        "restore_revision": restore_revision,
        "path": cloud_path,
        "token": api.csrf_token,   
        "conflict": "rename"
    }

    return api(url, http_method, data=data)
