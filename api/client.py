import requests
from dataclasses import dataclass
from urllib.parse import urljoin


@dataclass
class TestUser:
    email: str
    password: str
    name: str
    access_token: str | None = None
    __test__ = False


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/') + '/'
        self.api_base = urljoin(self.base_url, 'api/')

    def create_user(self, user: TestUser) -> TestUser:
        url = urljoin(self.api_base, 'auth/register')
        payload = {"email": user.email, "password": user.password, "name": user.name}
        resp = requests.post(url, json=payload, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        raw = (data.get('accessToken') or data.get('access_token') or '')
        parts = raw.split(' ', 1)
        token = parts[min(len(parts) - 1, 1)]
        user.access_token = token or None
        return user

    def delete_user(self, access_token: str | None) -> None:
        url = urljoin(self.api_base, 'auth/user')
        token = access_token or ''
        headers = {"Authorization": f"Bearer {token}"}
        requests.delete(url, headers=headers, timeout=20)
