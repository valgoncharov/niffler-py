import os

import pytest
from playwright.sync_api import Playwright, sync_playwright, Page
from python_test.data_helpers.api_helpers import UserApiHelper
from dotenv import load_dotenv
from faker import Faker


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

# Поменял фикстуру
# @pytest.fixture(scope="session")
# def app_user(envs):
#     return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope='session')
def app_user(envs, auth_url: str) -> tuple[str, str]:
    user_name, password = os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")
    UserApiHelper(auth_url).create_user(user_name=user_name, user_password=password)
    return user_name, password


@pytest.fixture(scope="session")
def fake_app_user():
    fake = Faker()

    fake_username = fake.user_name()  # Генерация случайного логина
    fake_password = fake.password(  # Генерация сложного пароля
        length=12,
        special_chars=True,
        digits=True,
        upper_case=True,
        lower_case=True,
    )

    return fake_username, fake_password  # Возвращает кортеж (логин, пароль)


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()


def login_user_by_ui(page, app_user, auth_url):
    username, password = app_user
    page.goto(f"{auth_url}login")
    page.fill("[name='username']", username)
    page.fill("[name='password']", password)
    page.click("button:has-text('Log in')")


@pytest.fixture()
def auth(page, frontend_url, app_user):
    username, password = app_user
    page.goto(f"{frontend_url}login")
    page.fill("[name='username']", username)
    page.fill("[name='password']", password)
    page.click("button:has-text('Log in')")


class Pages:
    main_page = pytest.mark.usefixtures("main_page")


@pytest.fixture()
def main_page(page, frontend_url, auth):
    page.goto(frontend_url)
