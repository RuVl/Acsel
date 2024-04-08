from aiogram.fsm.state import StatesGroup, State


class UserMenu(StatesGroup):
    START = State('start')
