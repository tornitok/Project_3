from .base_page import BasePage
from locators.auth import ResetPasswordLocators
import allure


class ResetPasswordPage(BasePage):
    @allure.step("Ожидать загрузку страницы сброса пароля")
    def wait_loaded(self):
        self._is_visible(ResetPasswordLocators.PASSWORD_INPUT)
        return self

    @allure.step("Показать/скрыть пароль (переключить видимость)")
    def click_toggle_visibility(self):
        self.click(ResetPasswordLocators.TOGGLE_PASSWORD_VISIBILITY, ensure_clickable=True)
        return self

    @allure.step("Проверить, что поле пароля в фокусе")
    def is_password_input_focused(self) -> bool:
        element = self._is_present(ResetPasswordLocators.TOGGLE_PASSWORD_VISIBILITY)
        classes = element.get_attribute("class") or ""
        return "input_status_active" in classes
