from pages.base_page import BasePage
from locators.auth import LoginLocators
import allure


class LoginPage(BasePage):
    @allure.step("Перейти на страницу восстановления пароля")
    def go_to_forgot_password(self):
        self.click(LoginLocators.FORGOT_PASSWORD_LINK)
        return self

    @allure.step("Ввести email: {email}")
    def enter_email(self, email: str):
        self.send_keys(LoginLocators.EMAIL_INPUT, email)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password: str):
        self.send_keys(LoginLocators.PASSWORD_INPUT, password)
        return self

    @allure.step("Отправить форму входа")
    def submit(self):
        self.click(LoginLocators.SUBMIT_BUTTON)
        self._is_not_visible(LoginLocators.SUBMIT_BUTTON)
        return self

    @allure.step("Войти в систему через форму")
    def login(self, email: str, password: str):
        return self.enter_email(email).enter_password(password).submit()

    # --- page state helpers ---
    @allure.step("Ожидать загрузку страницы входа")
    def wait_loaded(self):
        """Wait until login page main input is visible."""
        self._is_visible(LoginLocators.EMAIL_INPUT)
        return self

    @allure.step("Проверить, что страница входа открыта")
    def is_open(self) -> bool:
        """Best-effort check that login page is open without direct driver usage in tests."""
        url = (self.current_url() or "").lower()
        return ("login" in url) or self.has_any(LoginLocators.EMAIL_INPUT)
