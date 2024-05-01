from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import FSMI18nMiddleware
from aiogram.utils.i18n import gettext as _

from core.keyboards.common import main_menu_ckb
from core.keyboards.inline.products import choose_category2buy_ikb
from core.state_machines import BuyProductActions
from core.text.handlers import CommonMessages
from core.text.keyboards import MainMenuCKbMessages
from database import models
from database.enums import UserRights
from .buy import buy_router
from .create import create_router
from .paginator import paginator_router

products_router = Router()
products_router.include_routers(buy_router, create_router, paginator_router)


@products_router.message(
    CommandStart(),
    flags={'dialog': 'call start command'}
)
async def start_handler(msg: Message, db_user: models.User, state: FSMContext) -> Message:
    await state.clear()
    return await msg.answer(text=CommonMessages.greeting, reply_markup=main_menu_ckb(db_user))


@products_router.message(
    F.text.in_(MainMenuCKbMessages.common_replies()),
    flags={'dialog': f'sent command: {F.text}'}
)
async def main_menu_handler_user_replies(msg: Message, db_user: models.User, state: FSMContext, language: FSMI18nMiddleware) -> Message:
    await state.clear()

    match msg.text:
        case MainMenuCKbMessages.buy:
            if not db_user.rights & UserRights.CAN_BUY:
                return await msg.answer(_('Not allowed'))

            await state.set_state(BuyProductActions.SELECT_CATEGORY)
            keyboard = await choose_category2buy_ikb()
            return await msg.answer(CommonMessages.choose_category, reply_markup=keyboard)
        case MainMenuCKbMessages.support:
            return await msg.answer(CommonMessages.support)

        case MainMenuCKbMessages.english:
            await language.set_locale(state, 'en')
            return await start_handler(msg, db_user, state)
        case MainMenuCKbMessages.russian:
            await language.set_locale(state, 'ru')
            return await start_handler(msg, db_user, state)
