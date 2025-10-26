from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_chrome() -> webdriver.Chrome:
    options = ChromeOptions()
    # Use new headless mode for modern Chrome
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # Hint desired window size; we also enforce it after start for reliability
    options.add_argument("--window-size=1280,900")

    # Rely on Selenium Manager to resolve the ChromeDriver automatically
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_window_size(1280, 900)
    except Exception:
        # Best-effort; not critical in headless
        pass
    return driver


def create_firefox() -> webdriver.Firefox:
    options = FirefoxOptions()
    options.headless = True
    # These flags are recognized by Firefox when used via geckodriver,
    # but we'll enforce via set_window_size after start as well.
    options.add_argument("--width=1280")
    options.add_argument("--height=900")

    # Rely on Selenium Manager to resolve geckodriver automatically
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
