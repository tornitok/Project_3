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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    driver = item.funcargs.get("driver")

    should_attach = int((rep.when == "call") and rep.failed and (driver is not None))
    data = [
        ("screenshot", lambda d: d.get_screenshot_as_png(), allure.attachment_type.PNG),
        ("page_source", lambda d: d.page_source, allure.attachment_type.HTML),
    ] * should_attach

    for name, getter, att_type in data:
        allure.attach(getter(driver), name=name, attachment_type=att_type)
