from base.base_object import BaseObject
import allure


class BasePage(BaseObject):
    @allure.step("Открыть страницу: {base_url}/{path}")
    def open(self, base_url: str, path: str = ""):
        base = base_url.rstrip('/')
        tail = path.lstrip('/')
        url = base + '/' + tail
        self.open_url(url)
        return self
