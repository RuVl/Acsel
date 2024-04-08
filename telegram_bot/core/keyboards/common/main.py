from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.text.keyboards import MainMenu


def main_menu_ckb(**kwargs):
    kwargs.setdefault('resize_keyboard', True)
    kwargs.setdefault('one_time_keyboard', True)
    kwargs.setdefault('input_field_placeholder', str(MainMenu.placeholder))

    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text=str(MainMenu.buy)),
        KeyboardButton(text=str(MainMenu.support)),
        KeyboardButton(text=str(MainMenu.english)),
        KeyboardButton(text=str(MainMenu.russian))
    )

    builder.adjust(1, 1, 2)

    return builder.as_markup(**kwargs)
