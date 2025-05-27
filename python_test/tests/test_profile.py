from python_test.tests.conftest import login_user_by_ui


class TestProfile:

    def test_profile_page(self, page):
        login_user_by_ui(page)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="Profile").click()

        assert page.get_by_role("heading", name="Profile", level=2).is_visible()
        assert page.locator("label:has-text('Username')").is_visible()
        assert page.get_by_text("Name", exact=True).is_visible()

