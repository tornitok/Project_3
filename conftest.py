import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config import URL

from time import sleep
import uuid
from typing import Generator
from api.client import ApiClient, TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage


@pytest.fixture
def base_url() -> str:
    return URL.BASE_URL


def _create_chrome() -> webdriver.Chrome:
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def _create_firefox() -> webdriver.Firefox:
    options = FirefoxOptions()
    options.headless = True
    options.add_argument("-width=1280")
    options.add_argument("-height=900")
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


_BROWSER_FACTORY = {
    "chrome": _create_chrome,
    "firefox": _create_firefox,
}


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    create = _BROWSER_FACTORY[request.param]
    drv = create()
    drv.delete_all_cookies()
    yield drv
    drv.quit()


@pytest.fixture
def api(base_url) -> ApiClient:
    return ApiClient(base_url)


@pytest.fixture
def test_user(api: ApiClient) -> Generator[TestUser, None, None]:
    email = f"auto_{uuid.uuid4().hex[:8]}@example.com"
    password = "P@ssw0rd!123"
    name = "AutoUser"
    user = TestUser(email=email, password=password, name=name)
    user = api.create_user(user)
    try:
        yield user
    finally:
        if getattr(user, "access_token", None):
            api.delete_user(user.access_token)


@pytest.fixture
def create_simple_order(driver, base_url):
    def _create(user: TestUser) -> int:
        with allure.step("Авторизоваться и создать простой заказ"):
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
            sleep(5)
            order_number = constructor.get_order_number_from_modal()
            constructor.close_order_modal()
            return order_number
    return _create


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    driver = item.funcargs.get("driver")

    should_attach = int((rep.when == "call") and rep.failed and (driver is not None))
    data = [
        ("скриншот", lambda d: d.get_screenshot_as_png(), allure.attachment_type.PNG),
        ("html страницы", lambda d: d.page_source, allure.attachment_type.HTML),
    ] * should_attach

    for name, getter, att_type in data:
        allure.attach(getter(driver), name=name, attachment_type=att_type)
