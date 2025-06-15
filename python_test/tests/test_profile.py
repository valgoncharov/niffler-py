from python_test.tests.conftest import login_user_by_ui
from python_test.data_helpers.api_helpers import UserApiHelper

# Headers
NO_DATA_USERS = "There are no users yet"


class TestProfile:

    def test_profile_page(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="Profile").click()

        assert page.get_by_role("heading", name="Profile", level=2).is_visible()
        assert page.locator("label:has-text('Username')").is_visible()
        assert page.get_by_text("Name", exact=True).is_visible()


class TestMenuApp:
    def test_friends_page(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="Friends").click()

        assert page.get_by_role("heading", name="Friends", level=2).is_visible()
        assert page.get_by_role("heading", name="All people", level=2).is_visible()
        assert page.get_by_text(text=NO_DATA_USERS).is_visible()

    def test_all_people_page(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="All People").click()

        assert page.get_by_role("heading", name="Friends", level=2).is_visible()
        assert page.get_by_role("heading", name="All people", level=2).is_visible()
        assert page.get_by_text(text="Add friend")

    def test_add_friend_page(self, page, app_user):
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="All People").click()
        rows = page.get_by_role("row").filter(has=page.get_by_role("button", name="Add friend"))
        rows.first.get_by_role("button", name="Add friend").click()
        # page.get_by_role("button", name="Add friend").first.click()
        assert page.get_by_text("Waiting...")

    def test_add_friend_create_page(self, page, app_user):
        UserApiHelper.create_user(user_name="", user_password="")
        login_user_by_ui(page, app_user)
        page.get_by_role("button", name="Menu").click()
        page.get_by_role("link", name="All People").click()
        rows = page.get_by_role("row").filter(has=page.get_by_role("button", name="Add friend"))
        rows.first.get_by_role("button", name="Add friend").click()
        # page.get_by_role("button", name="Add friend").first.click()
        assert page.get_by_text("Waiting...")
