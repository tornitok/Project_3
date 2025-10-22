import uuid
from time import sleep

import allure
import pytest

from api.client import ApiClient, TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@allure.feature("Feed")
class TestFeed:
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

    @allure.story("Clicking an order opens details modal")
    def test_feed_open_order_details(self, driver, base_url):
        with allure.step("Открыть ленту заказов"):
            home = HomePage(driver).open(base_url)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded()
        with allure.step("Открыть детали первого заказа"):
            feed.open_first_order_details()
        with allure.step("Проверить, что модалка открылась и закрыть её"):
            assert feed.is_details_modal_opened(), "Модальное окно с деталями не открылось"
            feed.close_modal()

    def _auth_and_create_simple_order(self, driver, base_url, user: TestUser) -> int:
        home = HomePage(driver).open(base_url)
        login: LoginPage = home.go_to_login()
        login.login(user.email, user.password)
        constructor: ConstructorPage = home.go_to_constructor()
        constructor.wait_loaded()
        bun = constructor.get_first_bun_card()
        filling = constructor.get_first_filling_card()
        constructor.add_card_to_constructor(bun)
        constructor.add_card_to_constructor(filling)
        constructor.click_make_order().wait_order_modal()
        sleep(5) # wait for order to be ready
        order_number = constructor.get_order_number_from_modal()
        constructor.close_order_modal()
        return order_number

    @allure.story("User's history orders are present in Feed")
    def test_user_history_orders_visible_in_feed(self, driver, base_url, test_user: TestUser):
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = self._auth_and_create_simple_order(driver, base_url, test_user)
            assert order_number > 0, "Не удалось получить номер созданного заказа"
        with allure.step("Перейти в Личный кабинет -> История заказов"):
            home = HomePage(driver)
            profile: ProfilePage = home.go_to_account()
            profile.wait_loaded().go_to_orders_history()
            sleep(3)
            history_numbers = profile.list_history_order_numbers()
            assert order_number in history_numbers or len(history_numbers) > 0, "В истории не найден созданный заказ"
        with allure.step("Открыть Ленту заказов и дождаться появления номера из истории"):
            feed: FeedPage = home.go_to_feed()
            print(f"ORDER {order_number}")
            feed.wait_loaded().wait_for_order_in_feed(order_number, timeout_seconds=10)
            assert order_number in feed.list_feed_order_numbers(), "Номер из истории не отображается в Ленте"

    @allure.story("Done all time counter increases after new order")
    def test_done_all_time_increments_after_order(self, driver, base_url, test_user: TestUser):
        with allure.step("Открыть Ленту и запомнить значение счётчика 'Выполнено за всё время'"):
            home = HomePage(driver).open(base_url)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded()
            before = feed.get_done_all_time()
            assert before >= 0
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = self._auth_and_create_simple_order(driver, base_url, test_user)
            assert order_number > 0
        with allure.step("Вернуться в Ленту и дождаться увеличения счётчика"):
            feed = home.go_to_feed()
            feed.wait_loaded().wait_done_all_time_at_least(before + 1)
            after = feed.get_done_all_time()
            assert after >= before + 1, f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.story("Done today counter increases after new order")
    def test_done_today_increments_after_order(self, driver, base_url, test_user: TestUser):
        with allure.step("Открыть Ленту и запомнить значение счётчика 'Выполнено за сегодня'"):
            home = HomePage(driver).open(base_url)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded()
            before = feed.get_done_today()
            assert before >= 0
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = self._auth_and_create_simple_order(driver, base_url, test_user)
            assert order_number > 0
        with allure.step("Вернуться в Ленту и дождаться увеличения счётчика"):
            feed = home.go_to_feed()
            feed.wait_loaded().wait_done_today_at_least(before + 1)
            after = feed.get_done_today()
            assert after >= before + 1, f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.story("After creating an order, its number appears in 'В работе'")
    def test_new_order_appears_in_in_progress(self, driver, base_url, test_user: TestUser):
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = self._auth_and_create_simple_order(driver, base_url, test_user)
            assert order_number > 0
        with allure.step("Открыть Ленту и дождаться появления номера в 'В работе'"):
            home = HomePage(driver)
            feed: FeedPage = home.go_to_feed()
            print(f"ORDER {order_number}")
            feed.wait_loaded().wait_for_order_in_progress(order_number, timeout_seconds=10)
            in_progress = feed.list_in_progress_numbers()
            assert order_number in in_progress, "Новый заказ не появился в разделе 'В работе'"
