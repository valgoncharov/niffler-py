import pytest

from playwright.sync_api import Page

from python_test.model.RegisterPage import (
    LoginPage,
    BasePage,
    RegisterPage,
)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def base_page(page: Page) -> BasePage:
    return BasePage(page)


@pytest.fixture
def register_page(page: Page) -> RegisterPage:
    return RegisterPage(page)
