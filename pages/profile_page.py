from .base_page import BasePage
from locators.account import AccountLocators
from locators.auth import LoginLocators


class ProfilePage(BasePage):
    def wait_loaded(self):
        self._is_visible(AccountLocators.LOGOUT_BUTTON)
        return self

    def go_to_orders_history(self):
        self.click(AccountLocators.HISTORY_TAB)
        self.wait_url_contains_any(("order", "history"))
        return self

    def is_on_orders_history(self) -> bool:
        url = self.driver.current_url
        return any(p in url for p in ("order", "history"))

    def list_history_order_numbers(self) -> set[int]:
        cards = self.driver.find_elements(*AccountLocators.HISTORY_ORDER_CARD)
        numbers = [
            self.parse_int_from_optional_element(
                (c.find_elements(*AccountLocators.HISTORY_ORDER_NUMBER_REL) or [None])[0],
                default=-1,
            )
            for c in cards
        ]
        return set(filter(lambda n: n > 0, numbers))

    def logout(self):
        self.click(AccountLocators.LOGOUT_BUTTON)
        self._is_visible(LoginLocators.SUBMIT_BUTTON)
        from .login_page import LoginPage
        return LoginPage(self.driver)
