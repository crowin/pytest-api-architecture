import allure
from playwright.sync_api import BrowserContext, Cookie, Page

from core.common.config import Config
from core.common.user import User

@allure.step("Auth user {user.username}")
def auth_user_by_token(page: Page, user: User):
    page.context.add_cookies([Cookie(name="Authorization", value=f'Bearer {user.token}', domain=Config.BASE_URL)])
    page.reload()

@allure.step("Clear cookies")
def clear_browser_cookies(page: Page):
    page.context.clear_cookies()
    page.goto("/")
