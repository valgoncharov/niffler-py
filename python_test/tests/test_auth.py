from playwright.sync_api import Page
import re
from python_test.tests.conftest import login_user_by_ui
from faker import Faker

fake = Faker()

pattern = re.compile(r"Username .+ already exists")

# Header
REGISTER_TITLE = "text=Congratulations! You've registered!"
HISTORY_TITLE = "text=History of Spendings"
STATISTICS_TITLE = "text=Statistics"
DATA_TITLE = "text=There are no spendings"
WRONG_TITLE = "text=Неверные учетные данные пользователя"
# Errors
USERNAME_LENGTH = "Allowed username length should be from 3 to 50 characters"
PASSWORD_LENGTH = "Allowed password length should be from 3 to 12 characters"
PASSWORD_SHOULD = "Passwords should be equal"
# Fields
USERNAME_FIELD = "[name='username']"
PASSWORD_FIELD = "[name='password']"
PASSWORD_SUBMIT = "#passwordSubmit"
# Buttons
LOG_IN_BTN = "button:has-text('Log in')"
SIGN_UP_BTN = "button:has-text('Sign up')"
CREATE_ACC_BTN = "Create new account"


class TestAuth:

    def test_create_user(self, page: Page, frontend_url, app_user):
        username, password = app_user
        page.goto(f"{frontend_url}login")
        page.get_by_text(CREATE_ACC_BTN).click()
        page.fill(USERNAME_FIELD, username)
        page.fill(PASSWORD_FIELD, password)
        page.fill(PASSWORD_SUBMIT, password)
        page.click(SIGN_UP_BTN)

        assert page.text_content(REGISTER_TITLE)
        assert page.text_content("text=Sign in")

    def test_create_exist_user(self, page: Page, frontend_url, app_user):
        username, password = app_user
        page.goto(f"{frontend_url}login")
        page.get_by_text(CREATE_ACC_BTN).click()
        page.fill(USERNAME_FIELD, username)
        page.fill(PASSWORD_FIELD, password)
        page.fill(PASSWORD_SUBMIT, password)
        page.click(SIGN_UP_BTN)

        assert page.get_by_text(text=pattern, exact=False).is_visible()

    def test_login_by_exist_user(self, app_user, page: Page):
        login_user_by_ui(page, app_user)

        assert page.text_content(HISTORY_TITLE)
        assert page.text_content(STATISTICS_TITLE)
        assert page.text_content(DATA_TITLE)

    def test_logout_by_user(self, app_user, page: Page):
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_text(text="Sign out").click()
        page.get_by_role("button", name="Log out").click()

        h1 = page.locator("h1.header")
        # Проверка текста (если нужно удостовериться)
        assert h1.text_content() == "Log in"


class TestNegativeAuth:

    def test_login_by_not_exist_user(self, page: Page, frontend_url, fake_app_user):
        fake_username, fake_password = fake_app_user
        page.goto(f"{frontend_url}login")
        page.fill(USERNAME_FIELD, fake_username)
        page.fill(PASSWORD_FIELD, fake_password)
        page.click(LOG_IN_BTN)

        assert page.text_content(WRONG_TITLE)

    def test_create_not_valid_user(self, page: Page, frontend_url):
        page.goto(f"{frontend_url}login")
        page.get_by_text(CREATE_ACC_BTN).click()
        page.fill(USERNAME_FIELD, "1")
        page.fill(PASSWORD_FIELD, "1")
        page.fill(PASSWORD_SUBMIT, "1")
        page.click(SIGN_UP_BTN)

        assert page.get_by_text(text=USERNAME_LENGTH)
        assert page.get_by_text(text=PASSWORD_LENGTH)

    def test_create_not_valid_password(self, page: Page, frontend_url):
        user = fake.name()
        password = fake.password(length=13)
        page.goto(f"{frontend_url}login")
        page.get_by_text(CREATE_ACC_BTN).click()
        page.fill(USERNAME_FIELD, user)
        page.fill(PASSWORD_FIELD, password)
        page.fill(PASSWORD_SUBMIT, password)
        page.click(SIGN_UP_BTN)

        assert page.get_by_text(text=USERNAME_LENGTH).is_hidden()
        assert page.get_by_text(text=PASSWORD_SHOULD)
        assert page.get_by_text(text=PASSWORD_LENGTH)
#API