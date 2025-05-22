import pytest
from playwright.sync_api import Playwright, sync_playwright


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


def is_user_logged_in(page):
    page.goto("http://auth.niffler.dc:9000/login")
    page.fill("[name='username']", "usertest")
    page.fill("[name='password']", "Password123!")
    page.click("button:has-text('Log in')")
