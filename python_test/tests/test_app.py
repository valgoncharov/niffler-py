from python_test.tests.conftest import is_user_logged_in
from playwright.sync_api import Page


def test_add_new_spending(page):
    is_user_logged_in(page)
    page.get_by_text("New spending").click()
    page.fill("[name='amount']", "10")
    page.fill("[name='category']", "rest")
    page.fill("[name='description']", "Go to rest")
    page.click("#save")

    locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
    locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
    assert locator.is_visible()

def test_add_empty_spending(page):
    is_user_logged_in(page)
    page.get_by_text("New spending").click()
    page.fill("[name='amount']", "")
    page.fill("[name='category']", "")
    page.fill("[name='description']", "")
    page.click("#save")

    locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
    locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
    assert locator.is_visible()


def test_delete_spending(page):
    is_user_logged_in(page)
    page.locator('tr:has-text("rest") input[type="checkbox"]').click()
    page.click("#delete")

