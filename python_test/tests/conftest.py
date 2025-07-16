import os
import allure

import pytest
try:
    from _pytest.fixtures import FixtureDef
    from _pytest.python import FixtureRequest
    from _pytest.nodes import Item
except ImportError:
    from pytest import Item, FixtureDef, FixtureRequest
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from allure_commons.types import AttachmentType
from playwright.sync_api import Playwright, sync_playwright, Page
from python_test.data_helpers.api_helpers import UserApiHelper
from python_test.clients.spends_client import SpendsHttpClient
from python_test.databases.spend_db import SpendDb
from dotenv import load_dotenv
from python_test.model.config import Envs
from faker import Faker
from python_test.clients.kafka_client import KafkaClient


# def pytest_configure(config):
#     # Убедимся, что плагин allure зарегистрирован
#     if not config.pluginmanager.has_plugin("allure_listener"):
#         listener = AllureListener(config)
#         config.pluginmanager.register(listener, "allure_listener")


# def allure_logger(config) -> AllureReporter:
#     listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
#     return listener.allure_logger

# def allure_logger(config) -> AllureReporter:
#     listener = config.pluginmanager.get_plugin("allure_listener")
#     if listener is None:
#         # Если плагин не зарегистрирован, регистрируем его
#         listener = AllureListener(config)
#         config.pluginmanager.register(listener, "allure_listener")
#     return listener.allure_logger

# def allure_logger(config) -> AllureReporter:
#     listener = config.pluginmanager.get_plugin("allure_listener")
#     if listener is None:
#         raise RuntimeError("Allure listener not registered. Check allure-pytest installation")
#     return listener.allure_logger

#
# @pytest.hookimpl(hookwrapper=True, trylast=True)
# def pytest_runtest_call(item: Item):
#     yield
#     allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())
#
#
# @pytest.hookimpl(hookwrapper=True, trylast=True)
# def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
#     yield
#     logger = allure_logger(request.config)
#     item = logger.get_last_item()
#     if item:
#         scope_letter = fixturedef.scope[0].upper()
#         item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: Item):
    yield
    try:
        allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())
    except Exception as e:
        print(f"Could not set Allure title: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    try:
        with allure.step(f"Fixture {fixturedef.argname}"):
            pass
    except Exception as e:
        print(f"Could not create Allure step: {e}")


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(
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
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


@pytest.fixture(scope='session')
def app_user(envs: Envs) -> tuple[str, str]:
    user_name, password = os.getenv(
        "TEST_USERNAME"), os.getenv("TEST_PASSWORD")
    UserApiHelper(envs.auth_url).create_user(
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
def category(spends_client: SpendsHttpClient, request, spend_db: SpendDb):
    category_name = request.param
    # category_names = [category.category for category in current_categories]
    # if category_name not in category_names:
    category = spends_client.add_category(category_name)
    yield category.category
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(spends_client: SpendsHttpClient, request):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend
    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


def login_user_by_ui(page: Page, app_user, envs: Envs):
    username, password = app_user
    page.goto(f"{envs.auth_url}login")
    page.fill("[name='username']", username)
    page.fill("[name='password']", password)
    page.click("button:has-text('Log in')")


@pytest.fixture()
def auth(page, envs: Envs, app_user):
    username, password = app_user
    page.goto(f"{envs.frontend_url}login")
    page.fill("[name='username']", username)
    page.fill("[name='password']", password)
    page.click("button:has-text('Log in')")


class Pages:
    main_page = pytest.mark.usefixtures("main_page")


@pytest.fixture()
def main_page(page, frontend_url, auth):
    page.goto(frontend_url)


@pytest.fixture(scope="session")
def kafka(envs: Envs):
    """Взаимодействие с Kafka"""
    with KafkaClient(envs) as k:
        yield k
