from python_test.tests.conftest import login_user_by_ui
from python_test.data_helpers.api_helpers import UserApiHelper
from python_test.model.ProfilePage import ProfilePage
import allure


class TestProfile:

    @allure.title("Интерфейс страницы Профиль")
    def test_profile_page(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        ProfilePage.click_menu_btn()
        ProfilePage.click_profile_btn()

        assert ProfilePage.should_be_profile_title
        assert ProfilePage.should_be_username_field
        assert ProfilePage.should_be_name_field


class TestMenuApp:

    @allure.title("Интерфейс страницы Друзья")
    def test_friends_page(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        ProfilePage.click_menu_btn()
        ProfilePage.click_friends_btn()

        assert ProfilePage.should_be_friends_title
        assert ProfilePage.should_be_all_people_title
        assert ProfilePage.should_be_no_data_users_title

    @allure.title("Интерфейс страницы все пользователи")
    def test_all_people_page(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        ProfilePage.click_menu_btn()
        ProfilePage.click_all_people_btn()

        assert ProfilePage.should_be_friends_title
        assert ProfilePage.should_be_all_people_title
        assert ProfilePage.should_be_add_friend_btn

    @allure.title("Добавление друга")
    def test_add_friend_page(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        ProfilePage.click_menu_btn()
        ProfilePage.click_all_people_btn()
        ProfilePage.click_add_friend_btn()
        assert ProfilePage.should_be_waiting_process

    @allure.title("Процесс добавления друга")
    def test_add_friend_create_page(self, page, app_user, auth_url):
        UserApiHelper.create_user(user_name="", user_password="")
        login_user_by_ui(page, app_user, auth_url)
        ProfilePage.click_menu_btn()
        ProfilePage.click_all_people_btn()
        ProfilePage.click_add_friend_btn()
        assert ProfilePage.should_be_waiting_process
