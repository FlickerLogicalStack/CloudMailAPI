from .. import constants

def billing_rates(api, http_method):
    url = constants.API_BILLING_RATES_PATH

    data = {
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)
