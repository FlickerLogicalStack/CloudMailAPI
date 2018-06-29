from .. import constants

def user(api) -> dict:
    url = constants.API_USER_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, "get", params=data)

def user_space(api) -> dict:
    url = constants.API_USER_SPACE_PATH

    data = {
        "token": api.csrf_token
    }

    return api(url, "get", params=data)
