from python_test.tests.conftest import login_user_by_ui


class TestApp:

    def test_add_new_spending_rub(self, page):
        login_user_by_ui(page)
        page.get_by_text("New spending").click()
        page.fill("[name='amount']", "10")
        page.fill("[name='category']", "rest")
        page.fill("[name='description']", "Go to rest")
        page.click("#save")

        locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
        locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert locator.is_visible()

    def test_add_new_spending_usd(self, page):
        login_user_by_ui(page)
        page.get_by_text("New spending").click()
        page.fill("[name='amount']", "10")
        page.locator("#currency").click()
        page.get_by_role("option", name="USD").click()
        page.fill("[name='category']", "rest")
        page.fill("[name='description']", "Go to rest")
        page.click("#save")

        locator = page.locator("div.MuiAlert-message >> text=New spending is successfully created")
        locator.wait_for(state="visible", timeout=5000)  # ждать до 5 сек
        assert locator.is_visible()

    def test_add_empty_spending(self, page):
        login_user_by_ui(page)
        page.get_by_text("New spending").click()
        page.click("#save")

        locator = page.locator(".input__helper-text >> text=Amount has to be not less then 0.01")
        assert locator.is_visible()

        locator = page.locator(".input__helper-text >> text=Please choose category")
        assert locator.is_visible()

    def test_search_by_date_spending(self, page):
        login_user_by_ui(page)
        page.get_by_role("textbox", name="search").fill("rest")
        page.keyboard.press("Enter")
        assert page.locator('tr:has-text("rest")')

    def test_search_not_exist_spending(self, page):
        login_user_by_ui(page)
        page.get_by_role("textbox", name="search").fill("test")
        page.keyboard.press("Enter")
        page.is_visible("text=There are no spendings")

    def test_delete_spending(self, page):
        login_user_by_ui(page)
        page.locator('tr.MuiTableRow-root[role="checkbox"]').click()
        page.click("#delete")












