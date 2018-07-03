from .. import constants

def notify_applink(api, http_method, phone_number: str) -> dict:
    url = constants.API_APPLINK_PATH

    data = {
        "phone": phone_number,
        "token": api.csrf_token
    }

    return api(url, http_method, json=data)
