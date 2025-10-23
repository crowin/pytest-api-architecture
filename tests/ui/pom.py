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
    def product_by_name(self, name: str):
        return ProductElement(self.product_list().filter(has_text=name).first)

    @allure.step("Get product by index: {index}")
    def product_by_index(self, index: int = 0):
        return ProductElement(self.product_list().nth(index))

    @allure.step("Get pagination")
    def pagination(self):
        return Pagination(self.page)

    @allure.step("Open Pruducts page")
    def open(self):
        self.page.goto("/")

class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Get username input")
    def username_input(self):
        return self.page.get_by_test_id("username")

    @allure.step("Get password input")
    def password_input(self):
        return self.page.get_by_test_id("password")

    @allure.step("Get login button")
    def login_button(self):
        return self.page.get_by_test_id("login")

    @allure.step("Auth with {username}")
    def auth(self, username: str, password: str):
        self.username_input().fill(username)
        self.password_input().fill(password)
        self.login_button().click()

    @allure.step("Open Login page")
    def open(self):
        self.page.goto("/login")



