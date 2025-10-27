from .base_page import BasePage
from locators.auth import ForgotPasswordLocators
import allure


class ForgotPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Проверить, что открыта страница восстановления пароля")
    def is_opened(self) -> bool:
        """Проверяет, что открыта страница восстановления пароля."""
        return "forgot" in self.current_url()

    @allure.step("Ввести email для восстановления: {email}")
    def enter_email(self, email: str) -> "ForgotPasswordPage":
        """Вводит email в поле на странице восстановления."""
        self.send_keys(ForgotPasswordLocators.EMAIL_INPUT, email)
        return self

    @allure.step("Нажать кнопку 'Восстановить'")
    def submit_restore(self) -> "ForgotPasswordPage":
        """Нажимает кнопку 'Восстановить' (переход на следующую страницу проверяется в тестах)."""
        self.click(ForgotPasswordLocators.RESTORE_BUTTON)
        return self

    # Синоним по стилю примера: click_button -> submit_restore
    @allure.step("Нажать кнопку восстановления (синоним)")
    def click_button(self) -> "ForgotPasswordPage":
        return self.submit_restore()
