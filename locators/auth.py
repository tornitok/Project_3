from selenium.webdriver.common.by import By


class LoginLocators:
    # Ссылка на восстановление пароля на странице логина
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(., 'Восстановить')]")
    # Поля и кнопка логина
    EMAIL_INPUT = (
        By.XPATH,
        "//form//*[self::input and (@type='email' or @type='text') and (contains(translate(@placeholder,'EMAILПРОЧ','emailпроч'),'email') or @name='name' or @name='email')]"
    )
    PASSWORD_INPUT = (By.XPATH, "//form//input[@type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//form//button[normalize-space(.)='Войти']")


class ForgotPasswordLocators:
    # Поле ввода email на странице восстановления пароля
    EMAIL_INPUT = (By.XPATH, "//div[contains(@class, 'input')][.//label[normalize-space(text())='Email']]//input")
    # Кнопка "Восстановить"
    RESTORE_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and normalize-space(text())='Восстановить']")


class ResetPasswordLocators:
    # Поле ввода нового пароля (первое поле с типом password)
    PASSWORD_INPUT = (
        By.XPATH,
        "//div[contains(@class, 'input_type_password')]//input[@type='password' or @type='text']"
    )
    TOGGLE_PASSWORD_VISIBILITY = (
        By.XPATH,
        "//div[contains(@class, 'input_type_text') or contains(@class, 'input_type_password')]"
    )
