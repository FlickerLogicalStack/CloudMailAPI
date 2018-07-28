from typing import Iterable

def folder(
    api,
    url: str,
    http_method: str,
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
    url: str,
    http_method: str,
    cloud_path: str) -> dict:

    data = {
        "home": cloud_path,
        "conflict": "rename",
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)

def folder_find(
    api,
    url: str,
    http_method: str,
    finding: str,
    cloud_path: str,
    limit=10000) -> dict:

    data = {
        "q": finding,
        "path": cloud_path,
        "limit": limit,
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)

def folder_viruscan(
    api,
    url: str,
    http_method: str,
    hash_list: Iterable[str]) -> dict:

    data = {
        "hash_list": hash_list,
        "token": api.csrf_token
    }

    return api(url, http_method, json=data)
