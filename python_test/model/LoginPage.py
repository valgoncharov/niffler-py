# from locators import BasePageLocators as Locators
from playwright.async_api import Page


class LoginPage:
    def __init__(self, page: Page):
        super().__init__(page)
        # self.base_page = Locators