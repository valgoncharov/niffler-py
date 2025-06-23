from python_test.locators.login_page_locators import LoginPageLocators as Locators
from playwright.async_api import Page
import allure


class LoginPage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_page = LoginPage(page)

    @allure.step("Нажать на кнопку создать новый аккаунт")
    def click_create_account_btn(self):
        self.get_by_text(Locators.CREATE_ACC_BTN).click()

    @allure.step("Нажать на кнопку создать новый аккаунт")
    def click_sign_up_btn(self):
        self.get_by_text(Locators.SIGN_UP_BTN).click()

    @allure.step("Нажать на кнопку войти в аккаунт")
    def click_log_in_btn(self):
        self.get_by_text(Locators.LOG_IN_BTN).click()

    @allure.step("Заполнить поле Имя пользователя")
    def fill_user_field(self, username: str):
        self.fill(Locators.USERNAME_FIELD, username)

    @allure.step("Заполнить поле Пароль")
    def fill_password_field(self, password: str):
        self.fill(Locators.PASSWORD_FIELD, password)

    @allure.step("Заполнить поле Подтверждение пароля")
    def fill_password_submit_field(self, password: str):
        self.fill(Locators.PASSWORD_SUBMIT, password)

    @allure.step("Заполнение данных аккаунта")
    def fill_account_data(self):
        self.fill_user_field()
        self.fill_password_field()
        self.fill_password_submit_field()

    @allure.step("Должен быть предупреждающий загаловок")
    def should_be_wrong_title(self):
        self.text_content(Locators.WRONG_TITLE)

    @allure.step("Должен быть загаловок регитсрации")
    def should_be_register_title(self):
        self.text_content(Locators.REGISTER_TITLE)

    @allure.step("Должен быть загаловок статистики")
    def should_be_statistics_title(self):
        self.text_content(Locators.STATISTICS_TITLE)

    @allure.step("Должно быть предупреждение о длине имени")
    def should_be_alert_username_length(self):
        self.get_by_text(Locators.USERNAME_LENGTH).is_hidden()

    @allure.step("Должно быть предупреждение о длине пароля")
    def should_be_alert_password_length(self):
        self.get_by_text(Locators.PASSWORD_LENGTH)

    @allure.step("Должно быть предупреждение о соответствии пароля")
    def should_be_password_equal(self):
        self.get_by_text(Locators.PASSWORD_SHOULD)

    @allure.step("Должно быть кнопка Войти")
    def should_be_sign_up_btn(self):
        self.text_content("text=Sign in")

    @allure.step("Должно быть кнопка Войти")
    def should_be_log_in_btn(self):
        self.locator("h1.header").text_content() == "Log in"
        # Проверка текста (если нужно удостовериться)
        # h1.text_content() == "Log in"