import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.reset_password_page import ResetPasswordPage


@allure.feature("Password Recovery")
class TestPasswordRecovery:
    @allure.story("Navigate to Forgot Password from Login")
    def test_open_forgot_password_from_login(self, driver, base_url):
        with allure.step("Открыть главную и перейти к странице логина"):
            home = HomePage(driver).open(base_url)
            login_page = home.go_to_login()
        with allure.step("Перейти по ссылке 'Восстановить пароль'"):
            forgot_page = login_page.go_to_forgot_password()
        with allure.step("Проверить, что открылась страница восстановления пароля"):
            assert forgot_page.is_opened(), "Страница восстановления пароля не открылась"

    @allure.story("Submit email on Forgot Password")
    def test_submit_email_on_forgot_password(self, driver, base_url):
        with allure.step("Открыть страницу восстановления пароля через логин"):
            home = HomePage(driver).open(base_url)
            login_page: LoginPage = home.go_to_login()
            forgot_page: ForgotPasswordPage = login_page.go_to_forgot_password()
        with allure.step("Ввести email и нажать 'Восстановить'"):
            reset_page: ResetPasswordPage = (
                forgot_page
                .enter_email("autotest+recovery@example.com")
                .submit_restore()
            )
        with allure.step("Ждать появления поля для нового пароля"):
            reset_page.wait_loaded()

    @allure.story("Toggle eye icon focuses password field")
    def test_toggle_eye_focuses_password_field(self, driver, base_url):
        with allure.step("Дойти до страницы ввода нового пароля"):
            home = HomePage(driver).open(base_url)
            reset_page: ResetPasswordPage = (
                home
                .go_to_login()
                .go_to_forgot_password()
                .enter_email("autotest+recovery@example.com")
                .submit_restore()
            )
            reset_page.wait_loaded()
        with allure.step("Нажать на кнопку показать/скрыть пароль"):
            reset_page.click_toggle_visibility()
        with allure.step("Проверить, что поле пароля в фокусе"):
            assert reset_page.is_password_input_focused(), "Поле пароля не стало активным после клика по иконке"

