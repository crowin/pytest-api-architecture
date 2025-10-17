import allure
from playwright.sync_api import Page, Locator, expect

from core.common.config import Config


class ProductsPage:

    def __init__(self, page: Page):
        self.page = page
        self.products_list = page.locator(".shelf-container > .shelf-item")
        self.order_by_selector = page.locator(".sort select")
        self.vendors_filter = page.locator(".filters > .filters-available-size")

    @allure.step("Get product by {title} title")
    def get_product(self, title: str) -> 'ProductElement':
        return ProductElement(self.products_list.get_by_text(title))

    @allure.step("Add {product_title} product to cart")
    def add_to_cart(self, product_title: str):
        self.get_product(product_title).buy_button.click()

    @allure.step("Like {product_title} product")
    def like_product(self, product_title: str):
        self.get_product(product_title).like_button.click()

    @allure.step("Filter by vendors")
    def select_vendors(self, vendors: list):
        expect(self.vendors_filter).not_to_have_count(0)
        for vendor in vendors:
            self.vendors_filter.filter(has_text=vendor).first.click()

    @allure.step("Go to products page")
    def goto(self):
        self.page.goto(Config.BASE_DEMO_URL)


class ProductElement:

    def __init__(self, locator: Locator):
        self.locator = locator
        self.name = locator.locator(".shelf-item__title")
        self.price = locator.locator(".shelf-item__price")
        self.buy_button = locator.locator(".shelf-item__buy-btn")
        self.like_button = locator.locator(".shelf-stopper button")

