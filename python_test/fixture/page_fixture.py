import pytest

from playwright.sync_api import Page

from python_test.model.RegisterPage import RegisterPage
from python_test.model.LoginPage import LoginPage
from python_test.model.SpendingPage import SpendingPage
from python_test.model.BasePage import BasePage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def base_page(page: Page) -> BasePage:
    return BasePage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)
