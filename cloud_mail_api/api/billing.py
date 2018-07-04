def billing_rates(api, url, http_method):
    data = {
        "token": api.csrf_token,
    }

    return api(url, http_method, params=data)
