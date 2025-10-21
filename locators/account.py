from selenium.webdriver.common.by import By


class AccountLocators:
    # Ссылка в шапке "Личный кабинет"
    ACCOUNT_LINK = (By.XPATH, "//a[contains(@href, '/account') and .//p[contains(text(), 'Личный Кабинет')]]")

    # Вкладки в личном кабинете
    PROFILE_TAB = (By.XPATH, "//a[.//p[normalize-space(.)='Профиль'] or normalize-space(.)='Профиль']")
    HISTORY_TAB = (By.XPATH, "//a[.//p[normalize-space(.)='История заказов'] or normalize-space(.)='История заказов']")

    # Кнопки действий
    LOGOUT_BUTTON = (By.XPATH, "//button[@type='button' and normalize-space(.)='Выход']")

    # История заказов - элементы списка и номера
    HISTORY_ORDER_CARD = (
        By.XPATH,
        "//li[.//a[contains(@href,'/profile/orders') or contains(@href,'/account/order')]] | //a[contains(@href,'/profile/orders') or contains(@href,'/account/order')]/ancestor::*[self::li or self::div][1]"
    )
    HISTORY_ORDER_NUMBER_REL = (
        By.XPATH,
        ".//*[contains(@class,'digits') or contains(@class,'number') or starts-with(normalize-space(.), '#')][normalize-space()][1]"
    )
