from selenium.webdriver.common.by import By


class ConstructorLocators:
    # Заголовок конструктора
    TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Соберите бургер')]")

    # Табы категорий
    TAB_BUNS = (By.XPATH, "//div[contains(@class,'tab')][.//span[normalize-space(.)='Булки']]")
    TAB_SAUCES = (By.XPATH, "//div[contains(@class,'tab')][.//span[normalize-space(.)='Соусы']]")
    TAB_FILLINGS = (By.XPATH, "//div[contains(@class,'tab')][.//span[normalize-space(.)='Начинки']]")

    # Контейнер списка ингредиентов (видимая секция)
    VISIBLE_INGREDIENTS_SECTION = (
        By.XPATH,
        "(//section[.//h2[contains(@class,'title') or self::h2] and not(contains(@style,'display: none'))])[1]"
    )

    # Любая карточка ингредиента в текущей видимой секции
    ANY_INGREDIENT_CARD = (
        By.XPATH,
        "//section[.//h2]//a[contains(@href,'ingredient') or @draggable='true'] | //section[.//h2]//div[contains(@class,'ingredient') or contains(@class,'Ingredient')][@draggable='true']"
    )

    # Первая карточка булки/соуса/начинки в своей вкладке
    FIRST_BUN_CARD = (
        By.XPATH,
        "(//section[.//h2[contains(normalize-space(.),'Булки')] or .//span[contains(normalize-space(.),'Булки')]]//*[self::a or self::div][@draggable='true'])[1]"
    )
    FIRST_FILLING_CARD = (
        By.XPATH,
        "(//section[.//h2[contains(normalize-space(.),'Начинки')] or .//span[contains(normalize-space(.),'Начинки')]]//*[self::a or self::div][@draggable='true'])[1]"
    )

    # Счётчик на карточке (внутри карточки)
    CARD_COUNTER_REL = (
        By.XPATH,
        ".//*[contains(@class,'counter') or contains(@class,'Counter_counter') or contains(@class,'count')][normalize-space(number()) or normalize-space(text())]"
    )

    # Область конструктора (куда перетаскивают)
    CONSTRUCTOR_DROP = (By.XPATH, "//section[contains(@class,'BurgerConstructor') or contains(@class,'constructor')]")

    # Кнопка оформить заказ
    ORDER_BUTTON = (By.XPATH, "//button[.//span[normalize-space(.)='Оформить заказ'] or normalize-space(.)='Оформить заказ']")

    # Модалка деталей ингредиента
    INGREDIENT_MODAL = (
        By.XPATH,
        "//section[contains(@class,'Modal')]//*[contains(normalize-space(.),'Детали ингредиента') or contains(@class,'modal') and .//h2]//ancestor::section[contains(@class,'Modal') or contains(@role,'dialog')]"
    )
    MODAL_CLOSE = (By.XPATH, "//section[contains(@class,'Modal')]//*[self::button or self::svg or self::div][contains(@class,'close') or @aria-label='close' or @data-test='modal-close']")

    # Оверлей модалки
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_overlay') or contains(@class,'modal_overlay')]")

    # Универсальный элемент для закрытия модалки (кнопка закрытия или оверлей)
    MODAL_DISMISS = (
        By.XPATH,
        "(//section[contains(@class,'Modal')]//*[self::button or self::svg or self::div][contains(@class,'close') or @aria-label='close' or @data-test='modal-close'] | //div[contains(@class,'Modal_overlay') or contains(@class,'modal_overlay')])[1]"
    )

    # Контейнер любой модалки
    MODAL_ANY = (By.XPATH, "//section[contains(@class,'Modal')]")

    # Модалка заказа (успех)
    ORDER_MODAL = (By.XPATH, "//section[contains(@class,'Modal')]//*[contains(normalize-space(.),'идентификатор заказа') or contains(normalize-space(.),'номер заказа') or contains(@class,'order')]")
    # Номер заказа внутри модалки
    ORDER_NUMBER = (
        By.XPATH,
        "//section[contains(@class,'Modal')]//*[contains(@class,'digits') or contains(@class,'number')][normalize-space() and string(number(translate(normalize-space(.), '#№', '')))!='NaN'][1]"
    )
