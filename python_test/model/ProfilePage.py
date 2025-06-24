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

    @allure.step("Нажать на кнопку друзья")
    def click_friends_btn(self):
        self.get_by_role("link", name="Friends").click()

    @allure.step("Должно быть название страницы Профиль")
    def should_be_profile_title(self):
        self.get_by_role("heading", name="Profile", level=2).is_visible()

    @allure.step("Должно быть название поля пользователя")
    def should_be_username_field(self):
        self.locator("label:has-text('Username')").is_visible()

    @allure.step("Должно быть видно название поля Имя пользователя")
    def should_be_name_field(self):
        self.get_by_text("Name", exact=True).is_visible()

    @allure.step("Должно быть видно название вкладки Друзья")
    def should_be_friends_title(self):
        self.get_by_role("heading", name="Friends", level=2).is_visible()

    @allure.step("Должно быть видно название вкладки все пользователи")
    def should_be_all_people_title(self):
        self.get_by_role("heading", name="All people", level=2).is_visible()

    @allure.step("Должно быть видно название нет пользователей")
    def should_be_no_data_users_title(self):
        self.get_by_text(text=Locators.NO_DATA_USERS).is_visible()

    @allure.step("Нажать на кнопку добавить друга")
    def click_add_friend_btn(self):
        rows = self.get_by_role("row").filter(has=self.get_by_role("button", name="Add friend"))
        rows.first.get_by_role("button", name="Add friend").click()
        # page.get_by_role("button", name="Add friend").first.click()

    @allure.step("Должно быть видно кнопку добавить друга")
    def should_be_add_friend_btn(self):
        self.get_by_text(text="Add friend")

    @allure.step("Должно быть видно кнопку добавить друга")
    def should_be_add_friend_btn(self):
        self.get_by_text(text="Add friend")

    @allure.step("Должно быть видно кнопку добавить друга")
    def should_be_waiting_process(self):
        self.get_by_text("Waiting...")
