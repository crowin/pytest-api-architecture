import allure
from requests import Response

@allure.step("Verify that response is Ok")
def verify_ok_resp(resp: Response):
    assert resp.status_code in (200, 204), f"Response {resp.request.method} {resp.request.url} is wrong. Body: {resp.text}"

@allure.step("Verify that response is Bad")
def verify_bad_resp(resp: Response, error_msg = None):
    assert resp.status_code > 204, f"Response {resp.request.method} {resp.request.url} is successful"
    if error_msg:
        assert resp.json()["message"] == error_msg