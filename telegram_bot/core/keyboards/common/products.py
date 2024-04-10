from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.text.keyboards import MainMenuCKbMessages
from database.models import User, UserRights


def main_menu_ckb(db_user: User = None, **kwargs):
    kwargs.setdefault('resize_keyboard', True)
    kwargs.setdefault('one_time_keyboard', True)
    kwargs.setdefault('input_field_placeholder', str(MainMenuCKbMessages.placeholder))

    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=str(MainMenuCKbMessages.buy))
    ).row(
        KeyboardButton(text=str(MainMenuCKbMessages.support))
    )

    # Check db_user rights and add additional buttons
    if db_user is not None:
        additional_buttons = []
        if db_user.rights & UserRights.CAN_ADD_CATEGORY:
            additional_buttons.append(KeyboardButton(text=str(MainMenuCKbMessages.add_category)))

        if db_user.rights & UserRights.CAN_ADD_PRODUCT:
            additional_buttons.append(KeyboardButton(text=str(MainMenuCKbMessages.add_product)))

        if len(additional_buttons) > 0:
            builder.row(*additional_buttons)

    builder.row(
        KeyboardButton(text=str(MainMenuCKbMessages.english)),
        KeyboardButton(text=str(MainMenuCKbMessages.russian))
    )

    return builder.as_markup(**kwargs)
