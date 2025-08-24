import allure
import pytest

from core.api.carts_dto import CartsDto
from tests.api_assertions import verify_ok_resp
from tests.soft_assertion import SoftAssert
from tests.test_user import TestUser

@pytest.fixture(autouse=True, scope="function")
def add_allure_feature():
    allure.dynamic.feature("Products API /products")

@allure.title("User can get all carts")
def test_get_carts(basic_user_api):
    resp = basic_user_api.get_carts()
    verify_ok_resp(resp)
    carts = CartsDto(**resp.json()).carts

    assert len(carts) > 0, "Carts number should be more than 0"

    soft_assertions = SoftAssert()
    for cart in carts:
        soft_assertions.check(len(cart.products) > 0, f"{cart.id} cart should have products")
    soft_assertions.assert_all()


@allure.title("User can get cart by user id")
@pytest.mark.parametrize("user_id", [TestUser.BASIC_USER.user_id, TestUser.SECOND_USER.user_id])
def test_get_cart_by_id_with_user_id(user_id, basic_user_api):
    resp = basic_user_api.get_user_carts(user_id)
    verify_ok_resp(resp)
    cart = CartsDto(**resp.json()).carts[0]
    assert cart.user_id == user_id, "Cart user id should be equal to basic user id"
    assert len(cart.products) > 0, "Cart should have products"