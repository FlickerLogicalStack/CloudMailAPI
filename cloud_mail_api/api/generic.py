def generic_get_only_token(
    api,
    url,
    http_method) -> dict:

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)

def generic_post_only_token(
    api,
    url,
    http_method) -> dict:

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, data=data)
