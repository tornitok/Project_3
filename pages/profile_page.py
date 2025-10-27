from .base_page import BasePage
from locators.account import AccountLocators
import allure


class ProfilePage(BasePage):
    @allure.step("Ожидать загрузку страницы профиля")
    def wait_loaded(self):
        self._is_visible(AccountLocators.LOGOUT_BUTTON)
        return self

    @allure.step("Перейти в историю заказов")
    def go_to_orders_history(self):
        self.click(AccountLocators.HISTORY_TAB)
        self.wait_url_contains_any(("order", "history"))
        return self

    @allure.step("Проверить, что открыта история заказов")
    def is_on_orders_history(self) -> bool:
        url = self.current_url()
        return any(p in url for p in ("order", "history"))

    @allure.step("Получить номера заказов из истории")
    def list_history_order_numbers(self) -> set[int]:
        cards = self.find_elements(AccountLocators.HISTORY_ORDER_CARD)
        numbers = [
            self.parse_int_from_optional_element(
                (c.find_elements(*AccountLocators.HISTORY_ORDER_NUMBER_REL) or [None])[0],
                default=-1,
            )
            for c in cards
        ]
        return set(filter(lambda n: n > 0, numbers))

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.click(AccountLocators.LOGOUT_BUTTON)
        self._is_not_visible(AccountLocators.LOGOUT_BUTTON)

    @allure.step("Ожидать загрузку истории заказов")
    def wait_history_loaded(self):
        self.wait_until(lambda d: self.has_any(AccountLocators.HISTORY_ORDER_CARD))
        return self
