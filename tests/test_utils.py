import json
import shlex

import allure
import requests
from requests import Response


def short_url(response: Response):
    """
    Shortens a URL from a response to 40 characters if it exceeds that length.
    """
    return  f"{response.url[:40]}..." if len(response.url) > 40 else response.url


def patch_requests():
    """
    The original `requests.Session.request` method is replaced with a patched
    version that performs the same action but includes additional functionality for
    monitoring and debugging purposes through Allure reporting.
    """
    _original_request = requests.Session.request

    def patched_request(self, method, url, **kwargs):
        response = _original_request(self, method, url, **kwargs)

        curl_cmd = _request_to_curl(method, url, **kwargs)

        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
        }

        allure.attach(curl_cmd, name=f'Request {method} {short_url(url)}', attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(response_info, indent=2), name=f'Response  {method} {short_url(url)}', attachment_type=allure.attachment_type.JSON)

        return response

    requests.Session.request = patched_request


def _request_to_curl(method, url, **kwargs):
    """
    Converts HTTP request into the equivalent cURL command string representation.
    This method can be helpful for debugging or logging HTTP requests.

    :param method: HTTP method (e.g., GET, POST, PUT, DELETE)
    :param url: Request URL
    :param kwargs: Additional request parameters such as headers, data, or JSON
    :return: cURL command string representation
    :rtype: str
    """
    cmd = ["curl", "-X", method.upper(), shlex.quote(url)]

    headers = kwargs.get("headers") or {}
    for k, v in headers.items():
        cmd.extend(["-H", shlex.quote(f"{k}: {v}")])

    if "data" in kwargs and kwargs["data"] is not None:
        cmd.extend(["--data-raw", shlex.quote(str(kwargs["data"]))])

    if "json" in kwargs and kwargs["json"] is not None:
        json_data = json.dumps(kwargs["json"])
        cmd.extend(["-H", shlex.quote("Content-Type: application/json")])
        cmd.extend(["--data-raw", shlex.quote(json_data)])

    return " ".join(cmd)