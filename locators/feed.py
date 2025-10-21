from selenium.webdriver.common.by import By


class FeedLocators:
    # Заголовок ленты заказов
    TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Лента заказов') or contains(normalize-space(.), 'Лента')]")
    # Список/контейнер заказов
    ORDERS_LIST = (By.XPATH, "//section[contains(@class,'OrderFeed') or contains(@class,'feed') or .//ul[contains(@class,'OrderFeed')]]")

    # Карточки заказов в ленте
    ORDER_CARD = (
        By.XPATH,
        "//li[.//a[contains(@href,'/feed/')]] | //a[contains(@href,'/feed/')]/ancestor::*[self::li or self::div][1]"
    )
    ORDER_CARD_LINK_REL = (By.XPATH, ".//a[contains(@href,'/feed/')]")
    ORDER_CARD_NUMBER_REL = (
        By.XPATH,
        ".//*[contains(@class,'digits') or contains(@class,'number') or starts-with(normalize-space(.), '#')][normalize-space()][1]"
    )

    # Счётчики "Выполнено за всё время" и "Выполнено за сегодня"
    COUNTER_DONE_ALL_TIME = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Выполнено за все время') or contains(normalize-space(.), 'Выполнено за всё время')]/following::*[contains(@class,'digits') or contains(@class,'number')][1]"
    )
    COUNTER_DONE_TODAY = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Выполнено за сегодня')]/following::*[contains(@class,'digits') or contains(@class,'number')][1]"
    )

    # Раздел "В работе" (номера заказов в работе)
    IN_PROGRESS_NUMBERS = (
        By.XPATH,
        "//*[.//*[normalize-space(.)='В работе'] or .//h3[contains(normalize-space(.),'В работе')]]//*[contains(@class,'digits') or contains(@class,'number') or self::li or self::p][normalize-space()]"
    )

    # Модалка деталей заказа после клика по карточке (общее модальное окно)
    ORDER_DETAILS_MODAL = (
        By.XPATH,
        "//*[@role='dialog' or contains(@class,'Modal') or contains(@class,'modal')]"
    )
    # Элементы закрытия модалки
    MODAL_CLOSE = (
        By.XPATH,
        "//*[@role='dialog' or contains(@class,'Modal') or contains(@class,'modal')]//*[self::button or self::svg or self::div][contains(@class,'close') or @aria-label='close' or @data-test='modal-close']"
    )
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_overlay') or contains(@class,'modal_overlay')]")

    # Универсальный dismiss для модалки (кнопка или оверлей)
    MODAL_DISMISS = (
        By.XPATH,
        "((//*[@role='dialog' or contains(@class,'Modal') or contains(@class,'modal')]//*[self::button or self::svg or self::div][contains(@class,'close') or @aria-label='close' or @data-test='modal-close']) | //div[contains(@class,'Modal_overlay') or contains(@class,'modal_overlay')])[1]"
    )
