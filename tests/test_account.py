import allure

from api.client import TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@allure.feature("Личный кабинет")
class TestAccount:
    @allure.story("Переход в Личный кабинет открывает логин без авторизации")
    def test_open_account_redirects_to_login_when_unauthorized(self, driver, base_url):
        with allure.step("Открыть главную страницу"):
            home = HomePage(driver).open(base_url)
        with allure.step("Кликнуть по ссылке 'Личный кабинет' в шапке"):
            home.go_to_account()
        with allure.step("Ожидать, что открылась страница логина"):
            assert "login" in driver.current_url.lower()

    @allure.story("Открытие истории заказов в Личном кабинете")
    def test_open_orders_history(self, driver, base_url, test_user: TestUser):
        with allure.step("Открыть главную и перейти на страницу логина"):
            home = HomePage(driver).open(base_url)
            login: LoginPage = home.go_to_login()
        with allure.step("Авторизоваться под тестовым пользователем"):
            login.login(test_user.email, test_user.password)
        with allure.step("Перейти в 'Личный кабинет'"):
            profile: ProfilePage = home.go_to_account()
            profile.wait_loaded()
        with allure.step("Открыть вкладку 'История заказов'"):
            profile.go_to_orders_history()
        with allure.step("Проверить, что вкладка истории открыта"):
            assert profile.is_on_orders_history(), "Не удалось перейти в раздел 'История заказов'"

    @allure.story("Выход из аккаунта")
    def test_logout_from_account(self, driver, base_url, test_user: TestUser):
        with allure.step("Авторизоваться"):
            home = HomePage(driver).open(base_url)
            login: LoginPage = home.go_to_login()
            login.login(test_user.email, test_user.password)
        with allure.step("Открыть 'Личный кабинет' и выйти"):
            profile: ProfilePage = home.go_to_account()
            profile.wait_loaded()
            profile.logout()
        with allure.step("Проверить, что произошёл выход"):
            assert "login" in driver.current_url.lower(), "После выхода не открылась страница логина"
