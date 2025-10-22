from .base_page import BasePage
from locators.auth import ResetPasswordLocators


class ResetPasswordPage(BasePage):
    def wait_loaded(self):
        self._is_visible(ResetPasswordLocators.PASSWORD_INPUT)
        return self

    def click_toggle_visibility(self):
        self.click(ResetPasswordLocators.TOGGLE_PASSWORD_VISIBILITY, ensure_clickable=True)
        return self

    def is_password_input_focused(self) -> bool:
        element = self._is_present(ResetPasswordLocators.TOGGLE_PASSWORD_VISIBILITY)
        classes = element.get_attribute("class") or ""
        return "input_status_active" in classes
