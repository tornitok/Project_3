from selenium.webdriver.common.by import By


class HomeLocators:
    # Главная страница — кнопка входа
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space(.)='Войти в аккаунт']")

