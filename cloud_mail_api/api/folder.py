def folder(
    api,
    url,
    http_method,
    cloud_path: str,
    limit=100,
    offset=0,
    sort={"type":"name","order":"asc"}) -> dict:

    data = {
        "home": cloud_path,
        "token": api.csrf_token,
        "limit": limit,
        "offset": offset,
        "sort": sort,
    }

    return api(url, http_method, params=data)

def folder_add(
    api,
    url,
    http_method,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "conflict": "rename",
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)
