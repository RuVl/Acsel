from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import FSMI18nMiddleware

from core.keyboards import main_menu_ckb, choose_category_ikb
from core.state_machines import MainMenu
from core.text.handlers import CommonMessages
from core.text.keyboards import MainMenuCKbMessages
from core.text.utils import escape_md_v2 as md2
from database import models

common_router = Router()


@common_router.message(CommandStart())
async def start_handler(msg: types.Message, db_user: models.User):
    await msg.answer(text=md2(CommonMessages.greeting), reply_markup=main_menu_ckb(db_user))


@common_router.message(F.text.in_(MainMenuCKbMessages.user_replies()))
async def main_menu_handler_user_replies(msg: types.Message, db_user: models.User, state: FSMContext, language: FSMI18nMiddleware):
    match msg.text:
        case MainMenuCKbMessages.buy:
            await state.set_state(MainMenu.BUY)
            keyboard = await choose_category_ikb()
            await msg.answer(CommonMessages.choose_category, reply_markup=keyboard)
        case MainMenuCKbMessages.support:
            await msg.answer(CommonMessages.support)

        case MainMenuCKbMessages.english:
            await language.set_locale(state, 'en')
            await start_handler(msg, db_user)
        case MainMenuCKbMessages.russian:
            await language.set_locale(state, 'ru')
            await start_handler(msg, db_user)
