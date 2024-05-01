from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.text.keyboards import MainMenuCKbMessages_
from database.enums import UserRights
from database.models import User


def main_menu_ckb(db_user: User = None, **kwargs) -> ReplyKeyboardMarkup:
    kwargs.setdefault('is_persistent', True)
    kwargs.setdefault('resize_keyboard', True)
    kwargs.setdefault('one_time_keyboard', True)
    kwargs.setdefault('input_field_placeholder', MainMenuCKbMessages_.placeholder)

    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=MainMenuCKbMessages_.buy)
    ).row(
        KeyboardButton(text=MainMenuCKbMessages_.support)
    )

    # Check db_user rights and add additional buttons
    if db_user is not None:
        additional_buttons = []
        if db_user.rights & UserRights.CAN_ADD_CATEGORY:
            additional_buttons.append(KeyboardButton(text=MainMenuCKbMessages_.add_category))

        if db_user.rights & UserRights.CAN_ADD_PRODUCT:
            additional_buttons.append(KeyboardButton(text=MainMenuCKbMessages_.add_product))

        if db_user.rights & UserRights.CAN_ADD_FILE:
            additional_buttons.append(KeyboardButton(text=MainMenuCKbMessages_.add_product_files))

        if len(additional_buttons) > 0:
            builder.row(*additional_buttons)

    builder.row(
        KeyboardButton(text=MainMenuCKbMessages_.english),
        KeyboardButton(text=MainMenuCKbMessages_.russian)
    )

    return builder.as_markup(**kwargs)
