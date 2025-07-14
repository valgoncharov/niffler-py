from python_test.locators.spending_page_locators import SpendingPageLocators as Locators
from playwright.async_api import Page
import allure
from typing import Literal


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

    @allure.step("Нажать на кнопку валюта")
    def click_currency_btn(self):
        self.locator(Locators.CURRENCY_BTN).click()

    @allure.step("Выбрать {currency_choose} валюту")
    def click_on_choose_currency(self, currency_choose: Literal['RUB', 'USD', 'EUR', 'KZT']):
        self.get_by_role("option", name=currency_choose).click()

    @allure.step("Нажать на кнопку удалить в модальном окне")
    def click_delete_btn_on_banner(self):
        self.get_by_role("button", name="Delete").click()

    @allure.step("Нажать на кнопку удалить в модальном окне")
    def select_all_checkbox_rows(self):
        self.get_by_role(Locators.CHECKBOX_ALL, name="select all rows").click()

    @allure.step("Ввести данные в поле поиска")
    def fill_search_field(self, data: str):
        self.get_by_role("textbox", name="search").fill(data)
        self.keyboard.press("Enter")
        assert self.locator('tr:has-text({data})')

    @allure.step("Ввести данные в поле описание")
    def fill_description_field(self, description: str):
        self.locator(Locators.DESCRIPTION_FIELD).fill(description)

    @allure.step("Ввести данные в поле категория расходов")
    def fill_category_field(self, category_data: str):
        self.locator(Locators.CATEGORY_FIELD).fill(category_data)

    @allure.step("Ввести данные в поле количество")
    def fill_amount_field(self, amount: str):
        self.locator(Locators.AMOUNT_FIELD).fill(amount)

    @allure.step("Отображение баннера об успешном удалении расходов")
    def should_be_success_deleted_spending_banner(self):
        banner = self.locator(
            Locators.DELETED_BANNER)
        banner.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert banner.is_visible()

    @allure.step("Отображение баннера об успешном добавлении/создании расходов")
    def should_be_success_created_spending_banner(self):
        locator = self.locator(
            Locators.CREATED_BANNER)
        locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert locator.is_visible()

    @allure.step("Отображение подсказки/предупреждения об указании количества")
    def should_be_amount_alert(self):
        locator = self.locator(
            Locators.AMOUNT_ALERT)
        assert locator.is_visible()

    @allure.step("Отображение подсказки/предупреждения о выборе категории")
    def should_be_category_choose_alert(self):
        locator = self.locator(
            Locators.CATEGORY_ALERT)
        assert locator.is_visible()


