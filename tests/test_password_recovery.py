import allure
from config import URL
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage


@allure.feature("Восстановление пароля")
class TestPasswordRecovery:
    @allure.title("Переход на восстановление пароля со страницы логина")
    def test_open_forgot_password_from_login(self, driver):
        with allure.step("Открыть главную и перейти к странице логина"):
            home = HomePage(driver).open(URL.BASE_URL)
            home.go_to_login()
            login_page = LoginPage(driver)
        with allure.step("Перейти по ссылке 'Восстановить пароль'"):
            login_page.go_to_forgot_password()
            forgot_page = ForgotPasswordPage(driver)
        with allure.step("Проверить, что открылась страница восстановления пароля"):
            assert forgot_page.is_opened(), "Страница восстановления пароля не открылась"

    @allure.title("Отправка email на странице восстановления пароля")
    def test_submit_email_on_forgot_password(self, driver):
        with allure.step("Открыть страницу восстановления пароля через логин"):
            home = HomePage(driver).open(URL.BASE_URL)
            home.go_to_login()
            login_page = LoginPage(driver)
            login_page.go_to_forgot_password()
            forgot_page = ForgotPasswordPage(driver)
        with allure.step("Ввести email и нажать 'Восстановить'"):
            forgot_page.enter_email("autotest+recovery@example.com").submit_restore()
            reset_page = ResetPasswordPage(driver)
        with allure.step("Ждать появления поля для нового пароля"):
            reset_page.wait_loaded()

    @allure.title("Клик по иконке глаза переводит фокус на поле пароля")
    def test_toggle_eye_focuses_password_field(self, driver):
        with allure.step("Дойти до страницы ввода нового пароля"):
            home = HomePage(driver).open(URL.BASE_URL)
            home.go_to_login()
            login_page = LoginPage(driver)
            login_page.go_to_forgot_password()
            forgot_page = ForgotPasswordPage(driver)
            forgot_page.enter_email("autotest+recovery@example.com").submit_restore()
            reset_page = ResetPasswordPage(driver)
            reset_page.wait_loaded()
        with allure.step("Нажать на кнопку показать/скрыть пароль"):
            reset_page.click_toggle_visibility()
        with allure.step("Проверить, что поле пароля в фокусе"):
            assert reset_page.is_password_input_focused(), "Поле пароля не стало активным после клика по иконке"
