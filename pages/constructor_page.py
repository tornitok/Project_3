from .base_page import BasePage
from locators.constructor import ConstructorLocators as L
from selenium.webdriver.remote.webelement import WebElement


class ConstructorPage(BasePage):
    def wait_loaded(self):
        self._is_visible(L.TITLE)
        return self

    def open_any_ingredient_modal(self) -> None:
        card = self._is_present(L.ANY_INGREDIENT_CARD)
        self.js_click(card)
        self._is_visible(L.INGREDIENT_MODAL)

    def close_modal(self) -> None:
        self.click(L.MODAL_DISMISS, ensure_clickable=False)
        self._is_not_visible(L.INGREDIENT_MODAL)

    def _get_card_counter(self, card: WebElement) -> int:
        counters = card.find_elements(*L.CARD_COUNTER_REL)
        filtered = list(filter(lambda c: c.text.strip().isdigit(), counters))
        target = (filtered or [None])[0]
        return self.parse_int_from_optional_element(target, default=0)

    def get_first_filling_card(self) -> WebElement:
        return self._is_present(L.FIRST_FILLING_CARD)

    def get_first_bun_card(self) -> WebElement:
        return self._is_present(L.FIRST_BUN_CARD)

    def get_card_counter(self, card: WebElement) -> int:
        return self._get_card_counter(card)

    def add_card_to_constructor(self, card: WebElement) -> None:
        drop = self._is_present(L.CONSTRUCTOR_DROP)
        self.drag_and_drop_html5(card, drop)

    def click_make_order(self):
        self.click(L.ORDER_BUTTON)
        return self

    def wait_order_modal(self):
        self._is_visible(L.ORDER_MODAL)
        return self

    def get_order_number_from_modal(self) -> int:
        el = self._is_visible(L.ORDER_NUMBER)
        return self.parse_int_from_element(el, default=-1)

    def close_order_modal(self):
        self.click(L.MODAL_DISMISS, ensure_clickable=False)
        self._is_not_visible(L.ORDER_MODAL)
        return self
