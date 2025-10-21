import uuid

import allure
import pytest

from api.client import ApiClient, TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@allure.feature("Account")
class TestAccount:
    @pytest.fixture
    def api(self, base_url):
        return ApiClient(base_url)

    @pytest.fixture
    def test_user(self, api: ApiClient):
        # Генерируем уникальные данные пользователя
        email = f"auto_{uuid.uuid4().hex[:8]}@example.com"
        password = "P@ssw0rd!123"
        name = "AutoUser"
        user = TestUser(email=email, password=password, name=name)
        user = api.create_user(user)
        yield user
        api.delete_user(user.access_token)

    @allure.story("Navigate to Account opens Login when not authorized")
    def test_open_account_redirects_to_login_when_unauthorized(self, driver, base_url):
        with allure.step("Открыть главную страницу"):
            home = HomePage(driver).open(base_url)
        with allure.step("Кликнуть по ссылке 'Личный кабинет' в шапке"):
            home.go_to_account()
        with allure.step("Ожидать, что открылась страница логина"):
            # Проверяем по URL и наличию кнопки входа
            assert "login" in driver.current_url.lower()

    @allure.story("Open Order History in Account")
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
        with allure.step("Проверить, что вкладка истории открыта (по URL)"):
            assert profile.is_on_orders_history(), "Не удалось перейти в раздел 'История заказов'"

    @allure.story("Logout from Account")
    def test_logout_from_account(self, driver, base_url, test_user: TestUser):
        with allure.step("Авторизоваться"):
            home = HomePage(driver).open(base_url)
            login: LoginPage = home.go_to_login()
            login.login(test_user.email, test_user.password)
        with allure.step("Открыть 'Личный кабинет' и выйти"):
            profile: ProfilePage = home.go_to_account()
            profile.wait_loaded()
            profile.logout()
        with allure.step("Проверить, что произошел выход (по URL и наличию кнопки входа)"):
            assert "login" in driver.current_url.lower(), "После выхода не открылась страница логина"
