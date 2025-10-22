import pytest
from playwright.sync_api import sync_playwright

from core.common.config import Config


@pytest.fixture(scope="session")
def playwright_browser():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        pw.selectors.set_test_id_attribute("data-test-id")
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(playwright_browser):
    context = playwright_browser.new_context()
    page = context.new_page()
    page.goto(Config.BASE_URL)
    yield page
    context.close()
