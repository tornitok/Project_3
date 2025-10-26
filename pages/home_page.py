from .base_page import BasePage
from locators.account import AccountLocators
from locators.header import HeaderLocators
from locators.home import HomeLocators


class HomePage(BasePage):
    def open(self, base_url: str, path: str = ""):
        super().open(base_url, path)
        return self

    def go_to_login(self):
        self.click(HomeLocators.LOGIN_BUTTON)
        return self

    def go_to_account(self):
        self.click(AccountLocators.ACCOUNT_LINK)
        return self

    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        return self

    def go_to_feed(self):
        self.click(HeaderLocators.FEED_LINK)
        return self
