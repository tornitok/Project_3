from .base_page import BasePage
from locators.auth import LoginLocators
from .forgot_password_page import ForgotPasswordPage


class LoginPage(BasePage):
    def go_to_forgot_password(self):
        self.click(LoginLocators.FORGOT_PASSWORD_LINK)
        return ForgotPasswordPage(self.driver)

    def enter_email(self, email: str):
        self.send_keys(LoginLocators.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str):
        self.send_keys(LoginLocators.PASSWORD_INPUT, password)
        return self

    def submit(self):
        self.click(LoginLocators.SUBMIT_BUTTON)
        return self

    def login(self, email: str, password: str):
        return self.enter_email(email).enter_password(password).submit()
