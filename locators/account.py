from selenium.webdriver.common.by import By


class AccountLocators:
    # Вкладки в личном кабинете
    PROFILE_TAB = (By.XPATH, "//a[.//p[normalize-space(.)='Профиль'] or normalize-space(.)='Профиль']")
    HISTORY_TAB = (By.XPATH, "//a[.//p[normalize-space(.)='История заказов'] or normalize-space(.)='История заказов']")

    # Кнопки действий
    LOGOUT_BUTTON = (By.XPATH, "//button[@type='button' and normalize-space(.)='Выход']")

    # История заказов - элементы списка и номера
    HISTORY_ORDER_CARD = (
        By.XPATH,
        "//ul[contains(@class, 'OrderHistory_profileList')]//li[contains(@class, 'OrderHistory_listItem')]"
    )
    HISTORY_ORDER_NUMBER_REL = (
        By.XPATH,
        ".//p[@class='text text_type_digits-default' and starts-with(normalize-space(text()), '#')]"
    )
