from python_test.locators.spending_page_locators import SpendingPageLocators as Locators
from playwright.async_api import Page
import allure


class SpendingPage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.spending_page = SpendingPage(page)

    @allure.step("Нажать на кнопку сохранить")
    def click_save_btn(self):
        self.click(Locators.SAVE_BTN)

    @allure.step("Нажать на кнопку удалить")
    def click_delete_btn(self):
        self.click(Locators.DELETE_BTN)

    @allure.step("Нажать на кнопку создать новую запись по расходам")
    def click_new_spending_btn(self):
        self.get_by_text(Locators.NEW_SPENDING_BTN).click()

    @allure.step("Нажать на кнопку удалить")
    def click_currency_btn(self):
        self.locator(Locators.CURRENCY_BTN).click()

    @allure.step("Нажать на кнопку удалить")
    def click_delete_btn_on_banner(self):
        self.get_by_role("button", name="Delete").click()

    @allure.step("Ввести данные в поле поиска")
    def fill_search_field(self, data: str):
        self.get_by_role("textbox", name="search").fill(data)
        self.keyboard.press("Enter")
        assert self.locator('tr:has-text({data})')



