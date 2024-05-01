from aiogram.fsm.state import StatesGroup, State


class BuyProductActions(StatesGroup):
    SELECT_CATEGORY = State()
    SELECT_PRODUCT = State()

    CHOSE_QUANTITY = State()
    SURE_TO_BUY = State()


class CreateCategoryActions(StatesGroup):
    ADD_CATEGORY_NAME = State()

    SURE_CREATE_CATEGORY = State()


class CreateProductActions(StatesGroup):
    SELECT_CATEGORY = State()

    ADD_PRODUCT_NAME = State()
    ADD_PRODUCT_DESCRIPTION = State()
    ADD_PRODUCT_PRICE = State()

    SURE_CREATE_PRODUCT = State()


class CreateFileActions(StatesGroup):
    SELECT_CATEGORY = State()
    SELECT_PRODUCT = State()

    ADD_PRODUCT_FILES = State()
