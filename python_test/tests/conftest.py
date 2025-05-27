import os

import pytest
from playwright.sync_api import Playwright, sync_playwright
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def auth_url(envs):
    return os.getenv("AUTH_URL")


@pytest.fixture(scope="session")
def frontend_url(envs):
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


def login_user_by_ui(page, app_user):
    username, password = app_user
    page.goto("http://auth.niffler.dc:9000/login")
    page.fill("[name='username']", username)
    page.fill("[name='password']", password)
    page.click("button:has-text('Log in')")
