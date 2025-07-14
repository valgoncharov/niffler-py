class LoginPageLocators:
    # Header
    REGISTER_TITLE = "text=Congratulations! You've registered!"
    HISTORY_TITLE = "text=History of Spendings"
    STATISTICS_TITLE = "text=Statistics"
    DATA_TITLE = "text=There are no spendings"
    WRONG_TITLE = "text=Неверные учетные данные пользователя"
    # Errors/Alerts
    USERNAME_LENGTH = "Allowed username length should be from 3 to 50 characters"
    PASSWORD_LENGTH = "Allowed password length should be from 3 to 12 characters"
    PASSWORD_SHOULD = "Passwords should be equal"
    # Fields
    USERNAME_FIELD = "[name='username']"
    PASSWORD_FIELD = "[name='password']"
    PASSWORD_SUBMIT = "#passwordSubmit"
    # Buttons
    LOG_IN_BTN = "button:has-text('Log in')"
    SIGN_UP_BTN = "button:has-text('Sign up')"
    CREATE_ACC_BTN = "Create new account"
