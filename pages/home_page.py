from selenium.webdriver.common.by import By
from .base_page import BasePage
from locators.account import AccountLocators
from locators.header import HeaderLocators
from .login_page import LoginPage
from .profile_page import ProfilePage
from .constructor_page import ConstructorPage
from .feed_page import FeedPage


class HomePage(BasePage):
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space(.)='Войти в аккаунт']")

    def open(self, base_url: str, path: str = ""):
        super().open(base_url, path)
        return self

    def go_to_login(self):
        self.click(self.LOGIN_BUTTON)
        return LoginPage(self.driver)

    def go_to_account(self):
        self.click(AccountLocators.ACCOUNT_LINK)
        return ProfilePage(self.driver)

    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        return ConstructorPage(self.driver)

    def go_to_feed(self):
        self.click(HeaderLocators.FEED_LINK)
        return FeedPage(self.driver)
