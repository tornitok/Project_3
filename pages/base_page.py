from base.base_object import BaseObject


class BasePage(BaseObject):
    def open(self, base_url: str, path: str = ""):
        base = base_url.rstrip('/')
        tail = path.lstrip('/')
        url = base + '/' + tail
        self.driver.get(url)
        return self
