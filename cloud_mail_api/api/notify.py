def notify_applink(
	api,
	url,
	http_method,
	phone_number: str) -> dict:

    data = {
        "phone": phone_number,
        "token": api.csrf_token
    }

    return api(url, http_method, json=data)
