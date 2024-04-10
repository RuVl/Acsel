from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


async def choose_category_ikb():
    # TODO
    pass


def cancel_ikb():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=_('Cancel')))
    return builder.as_markup()
