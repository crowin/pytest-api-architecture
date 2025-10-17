import allure
import pytest

from core.api.user.auth_client import auth_user
from core.api.user.dto import TokenDto
from tests.api.api_assertions import verify_ok_resp, verify_bad_resp
from tests.test_user import TestUser

positive_user_provider = [(TestUser.FIRST_USER.username, TestUser.FIRST_USER.password), (TestUser.THIRD_USER.username, TestUser.THIRD_USER.password)]
negative_user_provider = [(TestUser.FIRST_USER.username, "wrong_password"), (TestUser.FIRST_USER.username, TestUser.FIRST_USER.username), (TestUser.THIRD_USER.username, ""), ("", "")]

@pytest.fixture(autouse=True, scope="function")
def add_allure_feature():
    allure.dynamic.feature("Users service API /users")

@allure.title("Valid users are authorized")
@pytest.mark.parametrize("username, password", positive_user_provider)
def test_verify_valid_users(username, password):
    resp = auth_user(username, password)
    verify_ok_resp(resp)
    TokenDto(**resp.json())

@allure.title("Invalid users are not authorized")
@pytest.mark.parametrize("username, password", negative_user_provider)
def test_verify_invalid_users(username, password):
    resp = auth_user(username, password)
    verify_bad_resp(resp)


