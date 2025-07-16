from python_test.locators.base_page_locators import BasePageLocators as Locators
from playwright.async_api import Page
import allure


class BasePage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.base_page = BasePage(page)

    def navigate(self):
        self.page.goto()

    @allure.step("Должен быть загаловок Истории")
    def should_be_history_title(self):
        self.text_content(Locators.HISTORY_TITLE)

    @allure.step("Должен быть загаловок Данных")
    def should_be_data_title(self):
        self.text_content(Locators.DATA_TITLE)
