# Stellar Burgers: E2E-тесты

Что включено:
- Page Object Model в каталоге `pages/` с базовым объектом в `base/`
- Локаторы сгруппированы в `locators/`
- Кросс-браузерный фикстур pytest (Chrome и Firefox) в `conftest.py`
- Отчёты Allure через `allure-pytest`
- Тесты сгруппированы по функциональности в `tests/`

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск тестов (Chrome и Firefox)

Браузеры запускаются в headless-режиме по умолчанию в фикстуре.

```bash
pytest -v --alluredir=allure-results
```

## Открыть отчёт Allure

```bash
allure serve allure-results
```

Примечания:
- Тестовые пользователи создаются и удаляются через API-фикстуры.
- Все элементы, используемые в тестах, описаны в Page Object'ах и локаторах.
- Тесты независимы и подходят для параллельного выполнения.
