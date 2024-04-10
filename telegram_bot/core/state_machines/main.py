from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    START = State('start')

    BUY = State('buy')


class PrivilegeActions(StatesGroup):
    ADD_CATEGORY = State('add_category')
    ADD_PRODUCT = State('add_product')
