# from locators import BasePageLocators as Locators
from playwright.async_api import Page


class BasePage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.base_page = Locators