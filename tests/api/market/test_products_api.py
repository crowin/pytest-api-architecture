import allure
import pytest

from core.api.market.market_client import MarketApi
from core.api.market.market_dto import CartDto, ProductsDto
from tests.api.api_assertions import verify_ok_resp
from tests.soft_assertion import SoftAssert
from tests.test_user import TestUser

@pytest.fixture(autouse=True, scope="function")
def add_allure_feature():
    allure.dynamic.feature("Market API /market")

@allure.title("User can get empty cart")
def test_empty_cart(basic_user_api, basic_user):
    basic_user_api.clear_cart()

    resp = basic_user_api.get_cart()
    verify_ok_resp(resp)
    cart = CartDto(**resp.json())

    assert cart.data is not None, "Cart data should not be None"

    soft = SoftAssert()
    soft.check(len(cart.data.items) == 0, "Cart should be empty")
    soft.check(cart.data.total_price == 0, "Cart total price should be zero")
    soft.assert_all()

@allure.title("User can get cart with products")
def test_cart_with_products(basic_user_api):
    basic_user_api.clear_cart()
    MarketApi(TestUser.THIRD_USER).clear_cart()

    products = ProductsDto(**basic_user_api.get_products().json())
    product_first = products.data.items[0]
    product_second = products.data.items[1]
    product_first_count = 2
    product_second_count = 1
    total_added_products = 2

    first_product_add_resp = basic_user_api.add_product_to_cart(product_first.id, product_first_count)
    second_product_add_resp = basic_user_api.add_product_to_cart(product_second.id, product_second_count)

    verify_ok_resp(first_product_add_resp)
    verify_ok_resp(second_product_add_resp)

    resp = basic_user_api.get_cart()
    verify_ok_resp(resp)
    cart = CartDto(**resp.json())

    assert cart.data is not None, "Cart data should not be None"
    assert len(cart.data.items) == total_added_products, f'Cart should contain only {total_added_products} products'
    soft = SoftAssert()
    soft.check(cart.data.items[0].product.id == product_first.id, "First product should be in cart")
    soft.check(cart.data.items[1].product.id == product_second.id, "Second product should be in cart")
    soft.check(cart.data.items[0].quantity == product_first_count, "First product should be added to cart twice")
    soft.check(cart.data.items[1].quantity == product_second_count, "Second product should be added to cart once")
    soft.check(cart.data.items[0].total_price == product_first.price * product_first_count, "First product price should be calculated correctly")
    soft.check(cart.data.items[1].total_price == product_second.price * product_second_count, "Second product price should be calculated correctly")
    soft.check(cart.data.total_price == (product_first_count * product_first.price) + (product_second_count * product_second.price), "Cart total price should be calculated correctly")
