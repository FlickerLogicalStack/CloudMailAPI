from .. import constants

def billing_rates(api):
    url = constants.API_BILLING_RATES_PATH

    data = {
        "token": api.csrf_token,
    }

    return api(url, "get", params=data)
