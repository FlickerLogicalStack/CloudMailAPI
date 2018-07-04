def user(
    api,
    url,
    http_method) -> dict:

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)

def user_space(
    api,
    url,
    http_method) -> dict:

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)
