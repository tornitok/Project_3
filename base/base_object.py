from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import urllib.parse


class BaseObject:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- ожидания ---
    def _is_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(ec.visibility_of_element_located(locator))

    def _is_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(ec.element_to_be_clickable(locator))

    def _is_present(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(ec.presence_of_element_located(locator))

    def _are_present(self, locator: tuple[str, str]) -> list[WebElement]:
        return self.wait.until(ec.presence_of_all_elements_located(locator))

    def _is_not_visible(self, locator: tuple[str, str]):
        return self.wait.until(ec.invisibility_of_element_located(locator))

    def _url_contains(self, text: str) -> bool:
        return self.wait.until(lambda d: text in d.current_url)

    def wait_url_contains_any(self, parts: tuple[str, ...] | list[str]) -> bool:
        return self.wait.until(lambda d: any(p in d.current_url for p in parts))

    # --- действия ---
    def click(self, locator: tuple[str, str], ensure_clickable: bool = True) -> None:
        pick = (self._is_present, self._is_clickable)
        element = pick[int(bool(ensure_clickable))](locator)
        self.js_click(element)

    def send_keys(self, locator: tuple[str, str], value: str, ensure_visible: bool = True) -> None:
        pick = (self._is_present, self._is_visible)
        element = pick[int(bool(ensure_visible))](locator)
        element.clear()
        element.send_keys(value)

    def get_current_url(self, wait_locator: tuple[str, str]) -> str:
        self._is_not_visible(wait_locator)
        return urllib.parse.unquote(self.driver.current_url)

    def get_text(self, locator: tuple[str, str]) -> str:
        return self._is_visible(locator).text

    def get_elements_count(self, locator: tuple[str, str], min_count: int | None = None) -> int:
        target = int(min_count or 1)
        self.wait.until(lambda d: len(d.find_elements(*locator)) >= target)
        return len(self.driver.find_elements(*locator))

    def parse_int_from_text(self, raw: str, default: int = -1) -> int:
        txt = (raw or "").strip()
        digits = ''.join(filter(lambda ch: ch.isdigit(), txt))
        return (digits and int(digits)) or default

    def parse_int_from_element(self, element: WebElement, default: int = -1) -> int:
        return self.parse_int_from_text(getattr(element, 'text', '') or '', default)

    def parse_int_from_optional_element(self, element: WebElement | None, default: int = -1) -> int:
        return self.parse_int_from_text((element and element.text) or '', default)

    def js_click(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].click();", element)

    def is_element_focused(self, element: WebElement) -> bool:
        return self.driver.execute_script("""
            const el = arguments[0];
            const active = document.activeElement;
            return el === active || active.contains(el) || el.contains(active);
        """, element)

    def drag_and_drop_html5(self, source: WebElement, target: WebElement) -> None:
        js = """
        const src = arguments[0];
        const tgt = arguments[1];
        const rect = el => el.getBoundingClientRect();
        const dt = new DataTransfer();
        function fire(el, type, clientX, clientY) {
          const evt = new DragEvent(type, {
            bubbles: true,
            cancelable: true,
            dataTransfer: dt,
            clientX, clientY
          });
          el.dispatchEvent(evt);
        }
        const s = rect(src);
        const t = rect(tgt);
        const sx = s.left + s.width/2;
        const sy = s.top + s.height/2;
        const tx = t.left + t.width/2;
        const ty = t.top + t.height/2;

        fire(src, 'dragstart', sx, sy);
        fire(tgt, 'dragenter', tx, ty);
        fire(tgt, 'dragover', tx, ty);
        fire(tgt, 'drop', tx, ty);
        fire(src, 'dragend', tx, ty);
        """
        self.driver.execute_script(js, source, target)
