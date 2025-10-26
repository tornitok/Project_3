from .base_page import BasePage
from locators.feed import FeedLocators


class FeedPage(BasePage):
    def wait_loaded(self):
        self._is_visible(FeedLocators.TITLE)
        return self

    def is_opened(self) -> bool:
        url_ok = "feed" in self.current_url()
        title_present = self.has_any(FeedLocators.TITLE)
        return url_ok or title_present

    def open_first_order_details(self):
        card = self._is_visible(FeedLocators.ORDER_CARD)
        links = card.find_elements(*FeedLocators.ORDER_CARD_LINK_REL)
        target = (links or [card])[0]
        self.scroll_into_view(target, block='center')
        self.js_click(target)
        self._is_present(FeedLocators.ORDER_DETAILS_MODAL)
        return self

    def close_modal(self):
        self.click(FeedLocators.MODAL_DISMISS, ensure_clickable=False)
        self._is_not_visible(FeedLocators.ORDER_DETAILS_MODAL)
        return self

    def is_details_modal_opened(self) -> bool:
        return self.has_any(FeedLocators.ORDER_DETAILS_MODAL)

    # --- counters helpers ---
    def get_done_all_time(self) -> int:
        el = self._is_visible(FeedLocators.COUNTER_DONE_ALL_TIME)
        return self.parse_int_from_element(el, default=-1)

    def get_done_today(self) -> int:
        el = self._is_visible(FeedLocators.COUNTER_DONE_TODAY)
        return self.parse_int_from_element(el, default=-1)

    def wait_done_all_time_at_least(self, value: int):
        self.wait.until(lambda d: self.get_done_all_time() >= value)
        return self

    def wait_done_today_at_least(self, value: int):
        self.wait.until(lambda d: self.get_done_today() >= value)
        return self

    def list_feed_order_numbers(self) -> set[int]:
        cards = self.find_elements(FeedLocators.ORDER_CARD)
        numbers = [
            self.parse_int_from_optional_element((c.find_elements(*FeedLocators.ORDER_CARD_NUMBER_REL) or [None])[0], default=-1)
            for c in cards
        ]
        return set(filter(lambda x: x > 0, numbers))

    def list_in_progress_numbers(self) -> set[int]:
        els = self.find_elements(FeedLocators.IN_PROGRESS_NUMBERS)
        numbers = [self.parse_int_from_element(el, default=-1) for el in els]
        return set(filter(lambda x: x > 0, numbers))

    def wait_for_order_in_feed(self, order_number: int, timeout_seconds: int = 30):
        self.wait_until(lambda d: order_number in self.list_feed_order_numbers(), timeout_seconds)
        return self

    def wait_for_order_in_progress(self, order_number: int, timeout_seconds: int = 30):
        self.wait_until(lambda d: order_number in self.list_in_progress_numbers(), timeout_seconds)
        return self
