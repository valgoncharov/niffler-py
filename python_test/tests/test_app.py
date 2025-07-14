import pytest
from python_test.tests.conftest import login_user_by_ui
from python_test.data_helpers.api_helpers import SpendsHttpClient
from python_test.model.BasePage import BasePage
from python_test.model.SpendingPage import SpendingPage
from conftest import Pages
import allure


class TestApp:

    @pytest.fixture(scope='class')
    def data(self, spends_client: SpendsHttpClient):
        spends_client.remove_all_spending()
        spends_client.add_spend('study', 500)
        yield
        spends_client.remove_all_spending()

    @Pages.main_page
    def test_spending_title_exists(self, page, app_user, frontend_url):
        assert BasePage.should_be_history_title

    @allure.title("Добавление нового расхода в рублях")
    def test_add_new_spending_rub(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.click_new_spending_btn()
        SpendingPage.fill_amount_field("10")
        SpendingPage.fill_category_field("rest")
        SpendingPage.fill_description_field("Go to rest")
        SpendingPage.click_save_btn()

        SpendingPage.should_be_success_created_spending_banner()

    @allure.title("Добавление нового расхода в долларах")
    def test_add_new_spending_usd(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.click_new_spending_btn()
        SpendingPage.fill_amount_field("10")
        SpendingPage.click_currency_btn()
        SpendingPage.click_on_choose_currency("USD")  # check
        SpendingPage.fill_category_field("rest")
        SpendingPage.fill_description_field("Go to rest")
        SpendingPage.click_save_btn()

        SpendingPage.should_be_success_created_spending_banner()

    @allure.title("Добавление пустых данных в расходах")
    def test_add_empty_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.click_new_spending_btn()
        SpendingPage.click_save_btn()

        SpendingPage.should_be_amount_alert()
        SpendingPage.should_be_category_choose_alert()

    @allure.title("Поиск по конкретным данным расходов")
    def test_search_by_date_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.fill_search_field(data="rest")

    @allure.title("Поиск несуществующих данных по расходам")
    def test_search_not_exist_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.fill_search_field(data="test")

        assert BasePage.should_be_data_title()

    @allure.title("Удалить данные по расходу")
    def test_delete_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        page.locator('tr.MuiTableRow-root[role="checkbox"]').first.click()
        SpendingPage.click_delete_btn()
        SpendingPage.click_delete_btn_on_banner()
        SpendingPage.should_be_success_deleted_spending_banner()

    @allure.title("Удалить все записи по расходам")
    def test_delete_all_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.select_all_checkbox_rows()
        SpendingPage.click_delete_btn()
        SpendingPage.click_delete_btn_on_banner()
        SpendingPage.should_be_success_deleted_spending_banner()

        assert BasePage.should_be_data_title


# TO DO
class TestApi:

    def test_spending_action(self, frontend_url):
        SpendsHttpClient.add_spend('test', 'RUB', 10, 1)

        assert SpendsHttpClient.get_ids_all_spending('test', 100)
