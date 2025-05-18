from playwright.async_api import Page


class RegisterPage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.base_page = Locators