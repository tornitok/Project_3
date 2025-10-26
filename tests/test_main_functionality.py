import allure

from config import URL
from api.client import TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage


@allure.feature("Основной функционал")
class TestMainFunctionality:
    @allure.story("Переход в Конструктор через шапку")
    def test_navigate_to_constructor_from_header(self, driver):
        home = HomePage(driver).open(URL.BASE_URL)
        home.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.wait_loaded()
        assert constructor.is_opened(), "Страница конструктора не открылась"

    @allure.story("Переход в Ленду через шапку")
    def test_navigate_to_feed_from_header(self, driver):
        home = HomePage(driver).open(URL.BASE_URL)
        home.go_to_feed()
        feed = FeedPage(driver)
        assert feed.is_opened()

    @allure.story("Модалка ингредиента открывается и закрывается")
    def test_ingredient_modal_open_close(self, driver):
        home = HomePage(driver).open(URL.BASE_URL)
        home.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.wait_loaded()
        with allure.step("Открыть модалку ингредиента"):
            constructor.open_any_ingredient_modal()
            assert constructor.is_ingredient_modal_opened(), "Модалка ингредиента не открылась"
        with allure.step("Закрыть модалку по крестику"):
            constructor.close_modal()
        assert not constructor.is_ingredient_modal_opened(), "Модалка ингредиента не закрылась"

    @allure.story("Счётчик ингредиента увеличивается при добавлении")
    def test_ingredient_counter_increments(self, driver):
        home = HomePage(driver).open(URL.BASE_URL)
        home.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.wait_loaded()
        card = constructor.get_first_filling_card()
        before = constructor.get_card_counter(card)
        constructor.add_card_to_constructor(card)
        after = constructor.get_card_counter(card)
        assert after == 2, f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.story("Авторизованный пользователь может оформить заказ")
    def test_logged_in_user_can_place_order(self, driver, test_user: TestUser):
        home = HomePage(driver).open(URL.BASE_URL)
        home.go_to_login()
        login = LoginPage(driver)
        login.login(test_user.email, test_user.password)
        home.go_to_constructor()
        constructor = ConstructorPage(driver)
        constructor.wait_loaded()
        bun = constructor.get_first_bun_card()
        filling = constructor.get_first_filling_card()
        constructor.add_card_to_constructor(bun)
        constructor.add_card_to_constructor(filling)
        constructor.click_make_order().wait_order_modal()
        order_number = constructor.get_order_number_from_modal()
        assert order_number > 0, f"Некорректный номер заказа: {order_number}"
