import uuid

import allure
import pytest

from api.client import ApiClient, TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage


@allure.feature("Main Functionality")
class TestMainFunctionality:
    @allure.story("Navigate to Constructor via header")
    def test_navigate_to_constructor_from_header(self, driver, base_url):
        home = HomePage(driver).open(base_url)
        constructor: ConstructorPage = home.go_to_constructor()
        constructor.wait_loaded()

    @allure.story("Navigate to Feed via header")
    def test_navigate_to_feed_from_header(self, driver, base_url):
        home = HomePage(driver).open(base_url)
        feed: FeedPage = home.go_to_feed()
        assert feed.is_opened()

    @allure.story("Ingredient modal opens and closes")
    def test_ingredient_modal_open_close(self, driver, base_url):
        home = HomePage(driver).open(base_url)
        constructor: ConstructorPage = home.go_to_constructor()
        constructor.wait_loaded()
        with allure.step("Открыть модалку ингредиента"):
            constructor.open_any_ingredient_modal()
        with allure.step("Закрыть модалку по крестику"):
            constructor.close_modal()

    @allure.story("Ingredient counter increments when added")
    def test_ingredient_counter_increments(self, driver, base_url):
        home = HomePage(driver).open(base_url)
        constructor: ConstructorPage = home.go_to_constructor()
        constructor.wait_loaded()
        card = constructor.get_first_filling_card()
        before = constructor.get_card_counter(card)
        constructor.add_card_to_constructor(card)
        after = constructor.get_card_counter(card)
        assert after == 2, f"Счётчик не увеличился: было {before}, стало {after}"

    @pytest.fixture
    def api(self, base_url):
        return ApiClient(base_url)

    @pytest.fixture
    def test_user(self, api: ApiClient):
        email = f"auto_{uuid.uuid4().hex[:8]}@example.com"
        password = "P@ssw0rd!123"
        name = "AutoUser"
        user = TestUser(email=email, password=password, name=name)
        user = api.create_user(user)
        yield user
        api.delete_user(user.access_token)

    @allure.story("Logged-in user can place order")
    def test_logged_in_user_can_place_order(self, driver, base_url, test_user: TestUser):
        home = HomePage(driver).open(base_url)
        login: LoginPage = home.go_to_login()
        login.login(test_user.email, test_user.password)
        constructor: ConstructorPage = home.go_to_constructor()
        constructor.wait_loaded()
        # Собираем бургер: булка + начинка
        bun = constructor.get_first_bun_card()
        filling = constructor.get_first_filling_card()
        constructor.add_card_to_constructor(bun)
        constructor.add_card_to_constructor(filling)
        # Оформляем заказ
        constructor.click_make_order().wait_order_modal()
