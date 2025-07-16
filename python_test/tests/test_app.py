import pytest
from python_test.tests.conftest import login_user_by_ui
from python_test.report_helper import Epic, Feature, Story
from python_test.data_helpers.api_helpers import SpendsHttpClient
from python_test.model.BasePage import BasePage
from python_test.model.SpendingPage import SpendingPage
from python_test.databases.spend_db import SpendDb
from python_test.model.config import Envs
from python_test.model.db.spend import SpendAdd, Category
from conftest import Pages
from python_test.marks import TestData
import allure
from datetime import datetime, timedelta

# TO DO Заменить envs


@allure.story(Epic)
@allure.story(Story.positive_cases)
class TestApp:

    @pytest.fixture(scope='class')
    def data(self, spends_client: SpendsHttpClient):
        spends_client.remove_all_spending()
        spends_client.add_spend('study', 500)
        yield
        spends_client.remove_all_spending()

    @Pages.main_page
    def test_spending_title_exists(self, page, app_user, envs):
        assert BasePage.should_be_history_title

    @allure.feature(Feature.spending)
    @allure.title("Добавление нового расхода в рублях")
    def test_add_new_spending_rub(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.click_new_spending_btn()
        SpendingPage.fill_amount_field("10")
        SpendingPage.fill_category_field("rest")
        SpendingPage.fill_description_field("Go to rest")
        SpendingPage.click_save_btn()

        SpendingPage.should_be_success_created_spending_banner()

    @allure.feature(Feature.spending)
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

    @allure.feature(Feature.spending)
    @allure.title("Добавление пустых данных в расходах")
    def test_add_empty_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.click_new_spending_btn()
        SpendingPage.click_save_btn()

        SpendingPage.should_be_amount_alert()
        SpendingPage.should_be_category_choose_alert()

    @allure.feature(Feature.search)
    @allure.title("Поиск по конкретным данным расходов")
    def test_search_by_date_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.fill_search_field(data="rest")

    @allure.feature(Feature.search)
    @allure.title("Поиск несуществующих данных по расходам")
    def test_search_not_exist_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.fill_search_field(data="test")

        assert BasePage.should_be_data_title()

    @allure.feature(Feature.spending)
    @allure.title("Удалить данные по расходу")
    def test_delete_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        page.locator('tr.MuiTableRow-root[role="checkbox"]').first.click()
        SpendingPage.click_delete_btn()
        SpendingPage.click_delete_btn_on_banner()
        SpendingPage.should_be_success_deleted_spending_banner()

    @allure.feature(Feature.spending)
    @allure.title("Удалить все записи по расходам")
    def test_delete_all_spending(self, page, app_user, auth_url):
        login_user_by_ui(page, app_user, auth_url)
        SpendingPage.select_all_checkbox_rows()
        SpendingPage.click_delete_btn()
        SpendingPage.click_delete_btn_on_banner()
        SpendingPage.should_be_success_deleted_spending_banner()

        assert BasePage.should_be_data_title

    @allure.feature(Feature.spending)
    @TestData.spend({
        'category': 'test_db',
        'amount': 100,
        'currency': 'KZT',
        'desc': 'Проверка данных в БД',
        'date': datetime(2025, 11, 30)
    })
    def test_data_spends_from_db(self, data, spend: SpendAdd, spend_db: SpendDb, envs: Envs):
        spend_from_db = spend_db.get_spend_by_id(spend_id=spend.id)
        assert spend_from_db.username == envs.test_username
        assert spend_from_db.amount == spend.amount
        assert spend_from_db.spend_date == datetime.strptime(spend.spendDate, "%Y-%m-%dT%H:%M:%S.%f%z").date()
        assert spend_from_db.currency == spend.currency
        assert spend_from_db.description == spend.description

    @allure.feature(Feature.category)
    @TestData.category({
        'category_name': 'test_db',
        'archived': False,
    })
    def test_data_category_from_db(self, category: Category, spend_db: SpendDb, envs: Envs):
        category_from_db = spend_db.get_category_by_id(category_id=category.id)

        assert category_from_db.archived == category.archived
        assert category_from_db.name == category.name
        assert category_from_db.username == envs.test_username

    @allure.feature(Feature.category)
    @TestData.category({
        'category_name': 'category_db_after_update',
        'archived': False,
    })
    def test_data_category_from_db_after_api_update(
            self,
            category: Category,
            spend_db: SpendDb,
            spends_client: SpendsHttpClient):

        new_category_name = 'api_update_category'
        new_attribute_archived = True

        spends_client.update_category(category.id, new_category_name, new_attribute_archived)
        category_from_db = spend_db.get_category_by_id(category_id=category.id)

        assert category_from_db.name == new_category_name
        assert category_from_db.archived == new_attribute_archived

    @TestData.spend({
        'category': 'Study',
        'amount': 100,
        'currency': 'USD',
        'desc': 'Coursera online courses',
        'date': datetime(2025, 11, 14)
    })
    def test_data_spend_from_db_after_api_update(
            self,
            data,
            spend: SpendAdd,
            spend_db: SpendDb,
            spends_client: SpendsHttpClient):

        new_category = 'Обучение'
        new_amount = 500
        new_currency = 'RUB'
        new_desc = 'Онлайн курсы'
        new_date = datetime(2025, 10, 12)

        update_spend = spends_client.update_spend(spend.id, new_category, new_amount, new_currency, new_desc, new_date)

        spend_from_db = spend_db.get_spend_by_id(spend_id=spend.id)
        category_from_db = spend_db.get_category_by_id(update_spend.category.id)

        assert spend_from_db.id.__str__() == spend.id
        assert category_from_db.name == new_category
        assert spend_from_db.amount == new_amount
        assert spend_from_db.currency == new_currency
        assert spend_from_db.description == new_desc
        assert spend_from_db.spend_date == new_date.date()


# TO DO
@allure.story(Story.api)
class TestApi:

    def test_spending_action(self):
        SpendsHttpClient.add_spend('test', 'RUB', 10, 1)

        assert SpendsHttpClient.get_ids_all_spending('test', 10)
