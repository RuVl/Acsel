from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import FSMI18nMiddleware

from core.keyboards import main_menu_ckb
from core.state_machines import UserMenu
from core.text.handlers import UserMessages
from core.text.keyboards import MainMenu
from core.text.utils import escape_md_v2 as md2

user_router = Router()

@user_router.message(CommandStart())
async def start_handler(msg: types.Message, state: FSMContext):
    await state.set_state(UserMenu.START)
    await msg.answer(text=md2(str(UserMessages.greeting)), reply_markup=main_menu_ckb())


@user_router.message(F.text.in_(MainMenu.replies()))
async def main_menu_handler(msg: types.Message, state: FSMContext, language: FSMI18nMiddleware):
    match msg.text:
        case MainMenu.buy:
            await msg.answer('Hello world\!')
        case MainMenu.support:
            await msg.answer('TODO')
        case MainMenu.russian:
            await language.set_locale(state, 'ru')
            await start_handler(msg, state)
        case MainMenu.english:
            await language.set_locale(state, 'en')
            await start_handler(msg, state)



