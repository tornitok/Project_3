from selenium.webdriver.common.by import By


class HeaderLocators:
    CONSTRUCTOR_LINK = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and .//p[normalize-space(text())='Конструктор']]")
    FEED_LINK = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and @href='/feed']//p[contains(text(), 'Лента Заказов')]")

