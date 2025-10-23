import allure
from playwright._impl._page import Page
from playwright.sync_api import Locator


class ProductElement:

    def __init__(self, product_locator: Locator):
        self.product = product_locator

    @allure.step("Get product name")
    def title(self):
        return self.product.locator(".font-semibold")

    @allure.step("Get product price")
    def price(self):
        return self.product.locator(".text-slate-600")

    @allure.step("Get product quantity")
    def quantity(self):
        return self.product.get_by_test_id("product-qty")

    @allure.step("Get product add to cart button")
    def add_to_cart_button(self):
        return self.product.get_by_test_id("product-add")

    @allure.step("Add product to cart")
    def add_to_cart(self, quantity: int = 1):
        self.quantity().fill(str(quantity))
        self.add_to_cart_button().click()


class Pagination:
    def __init__(self, page: Page):
        self.element = page.get_by_test_id("pagination")

    @allure.step("Get pagination status")
    def status(self):
        return self.element.locator("div").first

    @allure.step("Click next page")
    def click_next_page(self):
        self.element.get_by_test_id("next-page").click()

    @allure.step("Click prev page")
    def prev_page(self):
        self.element.get_by_test_id("prev-page").click()



class HeaderMenu:

    def __init__(self, page: Page):
        self.navigation: Locator = page.locator("header nav")

    @allure.step("Get login button")
    def login(self, user):
        return self.navigation.get_by_role("button", name="Login")

    @allure.step("Get logout button")
    def logout(self):
        return self.navigation.get_by_role("button", name="Logout")

    @allure.step("Get cart button")
    def cart(self):
        return self.navigation.get_by_test_id("cart-link")

    @allure.step("Get orders button")
    def orders(self):
        return self.navigation.get_by_test_id("orders-link")

    @allure.step("Get products button")
    def products(self):
        return self.navigation.get_by_test_id("products-link")