import pytest
import allure
from config import URL

import uuid
from typing import Generator
from api.client import ApiClient, TestUser
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.constructor_page import ConstructorPage
from drivers.browser_factory import BROWSER_FACTORY


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    create = BROWSER_FACTORY[request.param]
    drv = create()
    drv.delete_all_cookies()
    yield drv
    drv.quit()


@pytest.fixture
def api() -> ApiClient:
    return ApiClient(URL.BASE_URL)


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
def create_simple_order(driver):
    def _create(user: TestUser) -> int:
        with allure.step("Авторизоваться и создать простой заказ"):
            home = HomePage(driver).open(URL.BASE_URL)
            home.go_to_login()
            login = LoginPage(driver)
            login.login(user.email, user.password)
            home.go_to_constructor()
            constructor = ConstructorPage(driver)
            constructor.wait_loaded()
            bun = constructor.get_first_bun_card()
            filling = constructor.get_first_filling_card()
            constructor.add_card_to_constructor(bun)
            constructor.add_card_to_constructor(filling)
            constructor.click_make_order().wait_order_modal()
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
