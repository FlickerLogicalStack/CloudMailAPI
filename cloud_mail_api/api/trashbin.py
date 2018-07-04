def trashbin(
    api,
    url,
    http_method,
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
    url,
    http_method,
    restore_revision: int,
    cloud_path: str) -> dict:

    data = {
        "restore_revision": restore_revision,
        "path": cloud_path,
        "token": api.csrf_token,   
        "conflict": "rename"
    }

    return api(url, http_method, data=data)
