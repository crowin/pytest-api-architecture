import allure
import pytest
from playwright.sync_api import expect

from core.api.market.market_client import MarketApi
from core.api.market.market_dto import ProductsDto, CartDto
from tests.test_user import TestUser
from tests.ui.browser_helper import auth_user_by_token
from tests.ui.pom import ProductsPage

@pytest.fixture(autouse=True, scope="function")
def add_allure_feature():
    allure.dynamic.feature("Authorized user works with Products page")

@pytest.fixture(autouse=True, scope="function")
def auth_user(page, basic_user):
    auth_user_by_token(page.context, basic_user)

@allure.title("Products list is visible")
def test_products_are_visible(page, basic_user_api):
    resp = ProductsDto(**basic_user_api.get_products().json())
    product_page = ProductsPage(page)

    expect(product_page.product_list()).to_have_count(len(resp.data.items))

@allure.title("Products can be added to cart")
def test_add_to_cart(page, basic_user_api):
    product_first_count = 1
    product_second_count = 2
    products = ProductsDto(**basic_user_api.get_products().json()).data.items
    product_first = products[0]
    product_second = products[1]

    basic_user_api.clear_cart()
    MarketApi(TestUser.SECOND_USER).clear_cart()

    product_page = ProductsPage(page)
    product_page.product(product_first.title).add_to_cart(product_first_count)
    product_page.product(product_first.title).add_to_cart(product_second_count)

    actual_first_user_cart = CartDto(**basic_user_api.get_cart().json())
    actual_second_user_cart = CartDto(**MarketApi(TestUser.SECOND_USER).get_cart())

    assert len(actual_first_user_cart.data.items) == product_first_count + product_second_count, "Wrong number of products in cart"
    assert actual_first_user_cart.data.items[0].product.id == product_first.id, "Wrong product in cart"
    assert actual_first_user_cart.data.items[1].product.id == product_second.id, "Wrong product in cart"
    assert actual_second_user_cart.data.total_price == 0, "Second user cart should be empty"
    assert len(actual_second_user_cart.data.items) == 0, "Second user cart should be empty"