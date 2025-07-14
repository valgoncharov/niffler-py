class SpendingPageLocators:
    # Title
    DATA_TITLE = "text=There are no spendings"
    HISTORY_TITLE = "text=History of Spendings"
    # Buttons
    NEW_SPENDING_BTN = "New spending"
    DELETE_BTN = "#delete"
    SAVE_BTN = "#save"
    CURRENCY_BTN = "#currency"
    # Fields
    AMOUNT_FIELD = "[name='amount']"
    CATEGORY_FIELD = "[name='category']"
    DESCRIPTION_FIELD = "[name='description']"
    # Banners
    DELETED_BANNER = 'div.MuiTypography-body1:has-text("Spendings succesfully deleted")'
    CREATED_BANNER = "div.MuiAlert-message >> text=New spending is successfully created"
    # Alerts
    AMOUNT_ALERT = ".input__helper-text >> text=Amount has to be not less then 0.01"
    CATEGORY_ALERT = ".input__helper-text >> text=Please choose category"
    # Menu choose

    # Checkbox
    CHECKBOX_ALL = "checkbox"

