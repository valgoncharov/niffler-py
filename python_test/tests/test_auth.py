import allure
from playwright.sync_api import Page
import re
from python_test.tests.conftest import login_user_by_ui
from python_test.report_helper import Feature, Story
from faker import Faker
from python_test.model.LoginPage import LoginPage
from python_test.model.BasePage import BasePage

fake = Faker()

pattern = re.compile(r"Username .+ already exists")


@allure.story(Story.positive_cases)
class TestAuth:

    @allure.feature(Feature.sign_up)
    @allure.title("Создание нового аккаунта пользователя")
    def test_create_user(self, page: Page, frontend_url, app_user, ):
        username, password = app_user
        page.goto(f"{frontend_url}login")
        LoginPage.click_create_account_btn()
        LoginPage.fill_user_field()
        LoginPage.fill_password_field()
        LoginPage.fill_password_submit_field()
        LoginPage.click_sign_up_btn()

        assert LoginPage.should_be_register_title
        assert LoginPage.should_be_sign_up_btn

    @allure.feature(Feature.sign_up)
    @allure.title("Создание аккаунта существующего пользователя")
    def test_create_exist_user(self, page: Page, frontend_url, app_user):
        username, password = app_user
        page.goto(f"{frontend_url}login")
        LoginPage.click_create_account_btn()
        LoginPage.fill_account_data()
        LoginPage.click_sign_up_btn()

        assert page.get_by_text(text=pattern, exact=False).is_visible()

    @allure.feature(Feature.log_in)
    @allure.title("Вход существующим пользователем")
    def test_login_by_exist_user(self, app_user, page: Page, auth_url):
        login_user_by_ui(page, app_user, auth_url)

        assert BasePage.should_be_history_title
        assert LoginPage.should_be_statistics_title
        assert BasePage.should_be_data_title

    @allure.feature(Feature.log_out)
    @allure.title("Выход существующим пользователем")
    def test_logout_by_user(self, app_user, auth_url, page: Page):
        login_user_by_ui(page, app_user, auth_url)
        page.get_by_role("button", name="Menu").click()
        page.get_by_text(text="Sign out").click()
        page.get_by_role("button", name="Log out").click()

        assert LoginPage.should_be_log_in_btn


@allure.story(Story.negative_cases)
class TestNegativeAuth:

    @allure.feature(Feature.log_in)
    @allure.title("Вход несуществующим пользователем")
    def test_login_by_not_exist_user(self, page: Page, frontend_url, fake_app_user):
        fake_username, fake_password = fake_app_user
        page.goto(f"{frontend_url}login")
        LoginPage.fill_user_field(username=fake_username) #fake_username
        LoginPage.fill_password_field(password=fake_password) #fake_password
        LoginPage.click_log_in_btn()

        assert LoginPage.should_be_wrong_title

    @allure.feature(Feature.sign_up)
    @allure.title("Создание нового аккаунта с не валидными данными пользователя")
    def test_create_not_valid_user(self, page: Page, frontend_url):
        page.goto(f"{frontend_url}login")
        LoginPage.click_create_account_btn()
        LoginPage.fill_user_field() #(USERNAME_FIELD, "1")
        LoginPage.fill_password_field() #(PASSWORD_FIELD, "1")
        LoginPage.fill_password_submit_field() #(PASSWORD_SUBMIT, "1")
        LoginPage.click_sign_up_btn()

        assert LoginPage.should_be_alert_username_length
        assert LoginPage.should_be_alert_password_length

    @allure.feature(Feature.sign_up)
    @allure.title("Создание нового аккаунта с не валидным паролем пользователя")
    def test_create_not_valid_password(self, page: Page, frontend_url):
        user = fake.name()
        password = fake.password(length=13)
        page.goto(f"{frontend_url}login")
        LoginPage.click_create_account_btn()
        LoginPage.fill_account_data()

        assert LoginPage.should_be_alert_username_length
        assert LoginPage.should_be_password_equal
        assert LoginPage.should_be_alert_password_length
#API