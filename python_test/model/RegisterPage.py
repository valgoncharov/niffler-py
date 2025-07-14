from playwright.async_api import Page
from python_test.locators.register_page_locators import RegisterPageLocators
import allure


class RegisterPage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

    @allure.step("Заполнить креды")
    def fill_credentials(self, page, username, password):
        page.fill(RegisterPageLocators.USERNAME_FIELD, username)
        page.fill(RegisterPageLocators.PASSWORD_FIELD, password)
