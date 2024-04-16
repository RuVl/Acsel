from aiogram import Router, F, types
from aiogram.filters import MagicData
from aiogram.fsm.context import FSMContext

from core.state_machines import PrivilegeActions
from core.text.handlers import PrivilegeMessages
from core.text.keyboards import MainMenuCKbMessages
from database.enums import UserRights

privilege_router = Router()


@privilege_router.message(
    F.text == MainMenuCKbMessages.add_category,
    MagicData(F.db_user.rights & UserRights.CAN_ADD_CATEGORY)
)
async def main_menu_handler_add_category(msg: types.Message, state: FSMContext):
    await state.set_state(PrivilegeActions.ADD_CATEGORY)
    await msg.answer(text=PrivilegeMessages.ask_category_name)
