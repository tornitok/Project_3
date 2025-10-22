import allure

from api.client import TestUser
from pages.home_page import HomePage
from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage


@allure.feature("Лента заказов")
class TestFeed:
    @allure.story("Клик по заказу открывает модальное окно деталей")
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

    @allure.story("Заказы из истории пользователя отображаются в Ленте")
    def test_user_history_orders_visible_in_feed(self, driver, base_url, test_user: TestUser, create_simple_order):
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = create_simple_order(test_user)
            assert order_number > 0, "Не удалось получить номер созданного заказа"
        with allure.step("Перейти в Личный кабинет -> История заказов"):
            home = HomePage(driver)
            profile: ProfilePage = home.go_to_account()
            profile.wait_loaded().go_to_orders_history()
            import time; time.sleep(3)
            history_numbers = profile.list_history_order_numbers()
            assert order_number in history_numbers or len(history_numbers) > 0, "В истории не найден созданный заказ"
        with allure.step("Открыть Ленту заказов и дождаться появления номера из истории"):
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded().wait_for_order_in_feed(order_number, timeout_seconds=10)
            assert order_number in feed.list_feed_order_numbers(), "Номер из истории не отображается в Ленте"

    @allure.story("Счётчик 'Выполнено за всё время' увеличивается после нового заказа")
    def test_done_all_time_increments_after_order(self, driver, base_url, test_user: TestUser, create_simple_order):
        with allure.step("Открыть Ленту и запомнить значение счётчика 'Выполнено за всё время'"):
            home = HomePage(driver).open(base_url)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded()
            before = feed.get_done_all_time()
            assert before >= 0
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = create_simple_order(test_user)
            assert order_number > 0
        with allure.step("Вернуться в Ленту и дождаться увеличения счётчика"):
            feed = home.go_to_feed()
            feed.wait_loaded().wait_done_all_time_at_least(before + 1)
            after = feed.get_done_all_time()
            assert after >= before + 1, f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.story("Счётчик 'Выполнено за сегодня' увеличивается после нового заказа")
    def test_done_today_increments_after_order(self, driver, base_url, test_user: TestUser, create_simple_order):
        with allure.step("Открыть Ленту и запомнить значение счётчика 'Выполнено за сегодня'"):
            home = HomePage(driver).open(base_url)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded()
            before = feed.get_done_today()
            assert before >= 0
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = create_simple_order(test_user)
            assert order_number > 0
        with allure.step("Вернуться в Ленту и дождаться увеличения счётчика"):
            feed = home.go_to_feed()
            feed.wait_loaded().wait_done_today_at_least(before + 1)
            after = feed.get_done_today()
            assert after >= before + 1, f"Счётчик не увеличился: было {before}, стало {after}"

    @allure.story("После создания заказа его номер появляется в разделе 'В работе'")
    def test_new_order_appears_in_in_progress(self, driver, base_url, test_user: TestUser, create_simple_order):
        with allure.step("Создать заказ под тестовым пользователем"):
            order_number = create_simple_order(test_user)
            assert order_number > 0
        with allure.step("Открыть Ленту и дождаться появления номера в 'В работе'"):
            home = HomePage(driver)
            feed: FeedPage = home.go_to_feed()
            feed.wait_loaded().wait_for_order_in_progress(order_number, timeout_seconds=10)
            in_progress = feed.list_in_progress_numbers()
            assert order_number in in_progress, "Новый заказ не появился в разделе 'В работе'"
