from python_test.locators.profile_page_locators import ProfilePageLocators as Locators
from playwright.async_api import Page
import allure


class ProfilePage(Page):
    def __init__(self, page: Page):
        super().__init__(page)
        self.profile_page = ProfilePage(page)

    @allure.step("Нажать на кнопку меню")
    def click_menu_btn(self):
        self.get_by_role("button", name="Menu").click()

    @allure.step("Нажать на кнопку профиль")
    def click_profile_btn(self):
        self.get_by_role("link", name="Profile").click()

    @allure.step("Нажать на кнопку все пользователи")
    def click_all_people_btn(self):
        self.get_by_role("link", name="All People").click()

    @allure.step("Должно быть название ")
    def should_be_profile_title(self):
        self.get_by_role("heading", name="Profile", level=2).is_visible()

    @allure.step("Нажать на кнопку все пользователи")
    def should_be_username_field(self):
        self.locator("label:has-text('Username')").is_visible()
