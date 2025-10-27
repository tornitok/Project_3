from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import allure


@allure.step("Создать экземпляр браузера Chrome (headless)")
def create_chrome() -> webdriver.Chrome:
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,900")
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(1280, 900)
    except Exception:
        pass
    return driver


@allure.step("Создать экземпляр браузера Firefox (headless)")
def create_firefox() -> webdriver.Firefox:
    options = FirefoxOptions()
    options.headless = True
    options.add_argument("--width=1280")
    options.add_argument("--height=900")
    driver = webdriver.Firefox(options=options)
    try:
        driver.set_window_size(1280, 900)
    except Exception:
        pass
    return driver


BROWSER_FACTORY = {
    "chrome": create_chrome,
    "firefox": create_firefox,
}
