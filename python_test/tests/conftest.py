import os

import pytest
from playwright.sync_api import Playwright, sync_playwright, Page
from python_test.data_helpers.api_helpers import UserApiHelper
from python_test.clients.spends_client import SpendsHttpClient
from python_test.databases.spend_db import SpendDb
from dotenv import load_dotenv
from python_test.model.config import Envs
from faker import Faker
from python_test.clients.kafka_client import KafkaClient


@pytest.fixture(scope="session")
def envs():
    load_dotenv()
    # maybe
    return Envs(
        frontend_url=os.getenv("FRONTEND_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        auth_url=os.getenv('AUTH_URL'),
        auth_secret=os.getenv("AUTH_SECRET"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD"),
        kafka_address=os.getenv("KAFKA_ADDRESS"),
        userdata_db_url=os.getenv('USERDATA_DB_URL'),
        soap_address=os.getenv("SOAP_ADDRESS"),
    )


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
def kafka_address(envs) -> str:
    return os.getenv("KAFKA_ADDRESS")

# Поменял фикстуру
# @pytest.fixture(scope="session")
# def app_user(envs):
#     return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope='session')
def app_user(envs, auth_url: str) -> tuple[str, str]:
    user_name, password = os.getenv(
        "TEST_USERNAME"), os.getenv("TEST_PASSWORD")
    UserApiHelper(auth_url).create_user(
        user_name=user_name, user_password=password)
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


@pytest.fixture(scope="session")
def spends_client(envs):
    return SpendsHttpClient(envs.gateway_url, envs.auth_secret, envs.test_username)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(spends_client, request, spend_db):
    category_name = request.param
    # category_names = [category.category for category in current_categories]
    # if category_name not in category_names:
    category = spends_client.add_category(category_name)
    yield category.category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(spends_client, request):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


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


@pytest.fixture(scope="session")
def kafka(envs):
    """Взаимодействие с Kafka"""
    with KafkaClient(envs) as k:
        yield k
