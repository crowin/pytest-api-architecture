import allure
import pytest
from playwright.sync_api import expect

from core.api.products.dto import ProductsDto, Product
from core.api.products.products_client import ProductsApi
from tests.ui.pom import ProductsPage

vendors_provider = [["Apple"], ["Samsung"], ["Apple", "Samsung"]]

@allure.feature("Products page")
@pytest.fixture(scope="function", autouse=True)
def allure_feature():
    pass

@pytest.fixture
def products_api():
    yield ProductsApi()


@allure.title("Products list is visible for unauthorized user")
def test_products_are_visible(page, products_api):
    resp = ProductsDto(**products_api.get_products().json())
    product_page = ProductsPage(page)
    expect(product_page.products_list).to_have_count(len(resp.products))


@pytest.mark.parametrize("vendors", vendors_provider)
@allure.title("Products list is filtered by vendors")
def test_filter_products_by_vendor(page, products_api, vendors):
    resp = ProductsDto(**products_api.get_products().json())
    #     expected_count = len([product for product in resp.products if product.available_sizes in vendors])
    expected_count = len([product for product in resp.products if set(product.available_sizes).intersection(vendors)])
    product_page = ProductsPage(page)
    product_page.select_vendors(vendors)

    expect(product_page.products_list).to_have_count(expected_count)

def test_bad_dto():
    ProductsDto(products=[Product(sku='123', available_sizes=['123'])])
