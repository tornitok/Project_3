from .base_page import BasePage
from locators.auth import ForgotPasswordLocators


class ForgotPasswordPage(BasePage):
    """Страница восстановления пароля.

    Методы возвращают текущую страницу; создание других страниц выполняется в тестах.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def is_opened(self) -> bool:
        """Проверяет, что открыта страница восстановления пароля."""
        return "forgot" in self.current_url()

    def enter_email(self, email: str) -> "ForgotPasswordPage":
        """Вводит email в поле на странице восстановления."""
        self.send_keys(ForgotPasswordLocators.EMAIL_INPUT, email)
        return self

    def submit_restore(self) -> "ForgotPasswordPage":
        """Нажимает кнопку 'Восстановить' (переход на следующую страницу проверяется в тестах)."""
        self.click(ForgotPasswordLocators.RESTORE_BUTTON)
        return self

    # Синоним по стилю примера: click_button -> submit_restore
    def click_button(self) -> "ForgotPasswordPage":
        return self.submit_restore()
