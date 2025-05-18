from playwright.sync_api import Page


def test_create_user(page: Page):
    page.goto("http://auth.niffler.dc:9000/login")
    page.get_by_text("Create new account").click()
    page.fill("[name='username']", "usertest")
    page.fill("[name='password']", "Password123!")
    page.fill("#passwordSubmit", "Password123!")
    page.click("button:has-text('Sign up')")
    assert page.text_content("text=Congratulations! You've registered!")
    assert page.text_content("text=Sign in")


def test_login_by_not_exist_user(page: Page):
    page.goto("http://auth.niffler.dc:9000/login")
    page.fill("[name='username']", "testuser")
    page.fill("[name='password']", "Password123!")
    page.click("button:has-text('Log in')")
    assert page.text_content("text=Неверные учетные данные пользователя")


#Новым пользователем(?)
def test_login_by_exist_user(page: Page):
    page.goto("http://auth.niffler.dc:9000/login")
    page.fill("[name='username']", "usertest")
    page.fill("[name='password']", "Password123!")
    page.click("button:has-text('Log in')")
    assert page.text_content("text=History of Spendings")
    assert page.text_content("text=Statistics")
    assert page.text_content("text=There are no spendings")
