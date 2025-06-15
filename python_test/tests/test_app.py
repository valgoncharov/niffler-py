import pytest
from python_test.tests.conftest import login_user_by_ui
from python_test.data_helpers.api_helpers import SpendsHttpClient

# Title
DATA_TITLE = "text=There are no spendings"
# Buttons
NEW_SPENDING_BTN = "New spending"
DELETE_BTN = "#delete"
SAVE_BTN = "#save"
CURRENCY_BTN = "#currency"
# Fields
AMOUNT_FIELD = "[name='amount']"
CATEGORY_FIELD = "[name='category']"


class TestApp:

    @pytest.fixture(scope='class')
    def data(self, spends_client: SpendsHttpClient):
        spends_client.remove_all_spending()
        spends_client.add_spend('study', 500)
        yield
        spends_client.remove_all_spending()

    def test_add_new_spending_rub(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_text(NEW_SPENDING_BTN).click()
        page.fill(AMOUNT_FIELD, "10")
        page.fill(CATEGORY_FIELD, "rest")
        page.fill("[name='description']", "Go to rest")
        page.click(SAVE_BTN)

        locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
        locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert locator.is_visible()

    def test_add_new_spending_usd(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_text(NEW_SPENDING_BTN).click()
        page.fill(AMOUNT_FIELD, "10")
        page.locator(CURRENCY_BTN).click()
        page.get_by_role("option", name="USD").click()
        page.fill(CATEGORY_FIELD, "rest")
        page.fill("[name='description']", "Go to rest")
        page.click(SAVE_BTN)

        locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
        locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert locator.is_visible()

    def test_add_empty_spending(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_text(NEW_SPENDING_BTN).click()
        page.click(SAVE_BTN)

        locator = page.locator(".input__helper-text >> text=Amount has to be not less then 0.01")
        assert locator.is_visible()

        locator = page.locator(".input__helper-text >> text=Please choose category")
        assert locator.is_visible()

    def test_search_by_date_spending(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("textbox", name="search").fill("rest")
        page.keyboard.press("Enter")
        assert page.locator('tr:has-text("rest")')

    def test_search_not_exist_spending(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("textbox", name="search").fill("test")
        page.keyboard.press("Enter")
        page.is_visible(DATA_TITLE)

    def test_delete_spending(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.locator('tr.MuiTableRow-root[role="checkbox"]').first.click()
        page.click(DELETE_BTN)
        page.get_by_role("button", name="Delete").click()
        banner = page.locator('div.MuiTypography-body1:has-text("Spendings succesfully deleted")')
        banner.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert banner.is_visible()

    def test_delete_all_spending(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("checkbox", name="select all rows").click()
        page.click(DELETE_BTN)
        page.get_by_role("button", name="Delete").click()
        banner = page.locator('div.MuiTypography-body1:has-text("Spendings succesfully deleted")')
        banner.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert banner.is_visible()
        assert page.get_by_text(DATA_TITLE)




