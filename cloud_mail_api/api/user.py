from .. import constants

def user(api, http_method) -> dict:
    url = constants.API_USER_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)

def user_space(api, http_method) -> dict:
    url = constants.API_USER_SPACE_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, http_method, params=data)
