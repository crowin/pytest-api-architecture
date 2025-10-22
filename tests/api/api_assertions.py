import allure
from requests import Response

from tests.test_utils import short_url


def verify_ok_resp(resp: Response):
    with allure.step(f"Verify {resp.request.method} {short_url(resp)} is Ok"):
        assert resp.status_code in (200, 204), f"Response is wrong. Code: {resp.status_code}, body: {resp.text}"

def verify_bad_resp(resp: Response, error_msg = None):
    with allure.step(f"Verify {resp.request.method} {short_url(resp)} is wrong"):
        assert resp.status_code > 204, f"Response is successful. Code: {resp.status_code}, body: {resp.text}"
        if error_msg:
            assert resp.json()["message"] == error_msg