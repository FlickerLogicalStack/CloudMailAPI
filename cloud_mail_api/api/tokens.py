from .. import errors

def tokens_csrf(
    api,
    url: str,
    http_method: str,
    resolve_nosdc=False) -> dict:

    response = api(url, http_method)
    if (response.get("status") == 403) and (response.get("body") == "nosdc") and (resolve_nosdc):
        sdc_response = api.sdc()
        if sdc_response:
            return api.tokens.csrf()
        else:
            raise errors.CloudMailSdcGettingError(f"Received unexpected status code: {sdc_response.status_code}")
    else:
        return response
