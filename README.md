# Stellar Burgers: E2E tests

What is included:
- Page Object Model under `pages/` with a base object in `base/`
- Locators grouped under `locators/`
- Cross-browser pytest fixture (Chrome + Firefox) in `conftest.py`
- Allure reporting via `allure-pytest`
- Tests grouped by feature under `tests/`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run tests (Chrome + Firefox)

Browsers run headless by default in the fixture.

```bash
pytest -v --alluredir=allure-results
```

## Open Allure report

```bash
allure serve allure-results
```

Notes:
- Test users are created and removed via API fixtures.
- All elements used in tests are described in Page Objects and Locators.
- Tests are independent and suitable for parallel execution.
