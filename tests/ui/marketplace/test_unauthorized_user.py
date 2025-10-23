import allure
import pytest

from tests.ui.browser_helper import clear_browser_cookies
from tests.ui.pom import ProductsPage, LoginPage
from playwright.sync_api import expect


@pytest.fixture(autouse=True, scope="function")
def add_allure_feature():
    allure.dynamic.feature("Unauthorized user works with product")

@pytest.fixture(autouse=True, scope="function")
def setup(page):
    clear_browser_cookies(page)

@allure.title("Products list is visible for unauthorized user")
def test_products_page(page):
    product_page = ProductsPage(page)

    assert product_page.product_list(), "Products list is visible"
    actual_product = product_page.product_by_index()

    expect(actual_product.price()).to_be_visible()
    expect(actual_product.title()).to_be_visible()
    expect(actual_product.quantity()).not_to_be_visible()
    expect(actual_product.add_to_cart_button()).not_to_be_visible()

@allure.title("User can go to Login page")
def test_login_page(page):
    ProductsPage(page).navigation().login().click()

    expect(LoginPage(page).login_button()).to_be_visible()


