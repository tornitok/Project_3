from .base_page import BasePage
from locators.auth import ForgotPasswordLocators
from .reset_password_page import ResetPasswordPage


class ForgotPasswordPage(BasePage):
    """Страница восстановления пароля.

    Методы оставлены совместимыми с текущими тестами, но добавлен синоним
    click_button() по аналогии с приведённым примером.
    """

    def __init__(self, driver):
        super().__init__(driver)

    def is_opened(self) -> bool:
        """Проверяет, что открыта страница восстановления пароля."""
        return "forgot" in self.driver.current_url

    def enter_email(self, email: str) -> "ForgotPasswordPage":
        """Вводит email в поле на странице восстановления."""
        self.send_keys(ForgotPasswordLocators.EMAIL_INPUT, email)
        return self

    def submit_restore(self) -> ResetPasswordPage:
        """Нажимает кнопку 'Восстановить' и ожидает перехода к вводу нового пароля."""
        self.click(ForgotPasswordLocators.RESTORE_BUTTON)
        return ResetPasswordPage(self.driver)

    # Синоним по стилю примера: click_button -> submit_restore
    def click_button(self) -> ResetPasswordPage:
        return self.submit_restore()
