from .base_page import BasePage
from locators.header import HeaderLocators
from locators.home import HomeLocators
import allure


class HomePage(BasePage):
    @allure.step("Открыть страницу: {path}")
    def open(self, base_url: str, path: str = ""):
        super().open(base_url, path)
        return self

    @allure.step("Перейти на страницу входа")
    def go_to_login(self):
        self.click(HomeLocators.LOGIN_BUTTON)
        return self

    @allure.step("Перейти в личный кабинет")
    def go_to_account(self):
        self.click(HeaderLocators.ACCOUNT_LINK)
        return self

    @allure.step("Перейти в конструктор")
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        return self

    @allure.step("Перейти в ленту заказов")
    def go_to_feed(self):
        self.click(HeaderLocators.FEED_LINK)
        return self
