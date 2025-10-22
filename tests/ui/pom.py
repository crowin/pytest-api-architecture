import allure
from playwright.sync_api import Page

from tests.ui.components import ProductElement, HeaderMenu, Pagination


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Get navigation menu")
    def navigation(self):
        return HeaderMenu(self.page)


class ProductsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get Products list")
    def product_list(self):
        return self.page.get_by_test_id("product-card")

    @allure.step("Get product by name: {name}")
    def product(self, name: str):
        return ProductElement(self.product_list().filter(has_text=name).first)

    @allure.step("Get pagination")
    def pagination(self):
        return Pagination(self.page)



