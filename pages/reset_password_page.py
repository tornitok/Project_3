from .base_page import BasePage
from locators.auth import ResetPasswordLocators


class ResetPasswordPage(BasePage):
    def wait_loaded(self):
        self._is_visible(ResetPasswordLocators.PASSWORD_INPUT)
        return self

    def click_toggle_visibility(self):
        # Иногда клик по кнопке может быть перехвачен, поэтому используем click с фолбэком на JS
        self.click(ResetPasswordLocators.TOGGLE_PASSWORD_VISIBILITY, ensure_clickable=True)
        return self

    def is_password_input_focused(self) -> bool:
        # Проверяем, что поле пароля в фокусе
        element = self._is_present(ResetPasswordLocators.PASSWORD_INPUT)
        return self.is_element_focused(element)

