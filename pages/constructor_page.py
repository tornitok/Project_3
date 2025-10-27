from .base_page import BasePage
from locators.constructor import ConstructorLocators as L
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class ConstructorPage(BasePage):
    @allure.step("Ожидать загрузку страницы конструктора")
    def wait_loaded(self):
        self._is_visible(L.TITLE)
        return self

    @allure.step("Проверить, что страница конструктора открыта")
    def is_opened(self) -> bool:
        # Страница конструктора считается открытой, когда виден заголовок
        return self.has_any(L.TITLE)

    @allure.step("Открыть модальное окно ингредиента")
    def open_any_ingredient_modal(self) -> None:
        card = self._is_present(L.ANY_INGREDIENT_CARD)
        self.js_click(card)
        self._is_visible(L.INGREDIENT_MODAL)

    @allure.step("Закрыть модальное окно ингредиента")
    def close_modal(self) -> None:
        self.click(L.MODAL_DISMISS, ensure_clickable=False)
        self._is_not_visible(L.INGREDIENT_MODAL)

    @allure.step("Проверить, что модальное окно ингредиента открыто")
    def is_ingredient_modal_opened(self) -> bool:
        return any(el.is_displayed() for el in self.driver.find_elements(*L.INGREDIENT_MODAL))

    def _get_card_counter(self, card: WebElement) -> int:
        counters = card.find_elements(*L.CARD_COUNTER_REL)
        filtered = list(filter(lambda c: c.text.strip().isdigit(), counters))
        target = (filtered or [None])[0]
        return self.parse_int_from_optional_element(target, default=0)

    @allure.step("Получить первую карточку начинки")
    def get_first_filling_card(self) -> WebElement:
        return self._is_present(L.FIRST_FILLING_CARD)

    @allure.step("Получить первую карточку булки")
    def get_first_bun_card(self) -> WebElement:
        return self._is_present(L.FIRST_BUN_CARD)

    @allure.step("Получить счётчик на карточке")
    def get_card_counter(self, card: WebElement) -> int:
        return self._get_card_counter(card)

    @allure.step("Добавить карточку в конструктор")
    def add_card_to_constructor(self, card: WebElement) -> None:
        drop = self._is_present(L.CONSTRUCTOR_DROP)
        self.drag_and_drop_html5(card, drop)

    @allure.step("Нажать кнопку оформления заказа")
    def click_make_order(self):
        self.click(L.ORDER_BUTTON)
        return self

    @allure.step("Ожидать модальное окно заказа")
    def wait_order_modal(self):
        self._is_visible(L.ORDER_MODAL)
        return self

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self) -> int:
        def valid_text(_):
            try:
                t = self._is_visible(L.ORDER_NUMBER).text.strip()
                return t if t.isdigit() and t != "9999" else False
            except StaleElementReferenceException:
                return False

        try:
            txt = WebDriverWait(self.driver, 10).until(valid_text)
            return int(txt)
        except TimeoutException:
            return -1

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        modal = self._is_present(L.ORDER_MODAL)
        dismiss_btn = self._is_present(L.MODAL_DISMISS)
        try:
            dismiss_btn.click()
        except Exception:
            self.js_click(dismiss_btn)
        try:
            self.wait.until(EC.staleness_of(modal))
        except TimeoutException:
            self._is_not_visible(L.ORDER_MODAL)

        return self