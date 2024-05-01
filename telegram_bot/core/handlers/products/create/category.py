import logging

from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from core.keyboards.inline import cancel_ikb, sure2create_ikb
from core.state_machines import CreateCategoryActions
from core.text.handlers import PrivilegeMessages, CategoryMessages
from core.text.keyboards import MainMenuCKbMessages
from database import models
from database.enums import UserRights
from database.methods.category import create_category
from database.validators import validate_category_name

category_router = Router()

logger = logging.getLogger('telegram')


@category_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_CATEGORY),
    F.text == MainMenuCKbMessages.add_category,
    flags={'dialog': 'began creating a new category name'}
)
async def add_category_handler(msg: Message, state: FSMContext) -> Message:
    await state.clear()
    await state.set_state(CreateCategoryActions.ADD_CATEGORY_NAME)
    return await msg.answer(text=PrivilegeMessages.ask_category_name, reply_markup=cancel_ikb())


@category_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_CATEGORY),
    F.text.not_in(MainMenuCKbMessages.all_replies()),
    CreateCategoryActions.ADD_CATEGORY_NAME,
    flags={'dialog': 'added a new category name'}
)
async def add_category_name_handler(msg: Message, state: FSMContext) -> Message:
    name = validate_category_name(msg.text)
    if not name:
        logger.warning(f'User ({msg.from_user.id}) tried to set invalid category name: {msg.text}')
        await msg.reply(PrivilegeMessages.invalid_category_name)
        return

    category = models.Category(name=name)
    logger.debug(f'User ({msg.from_user.id}) set category name: {category}')
    await state.update_data(category=category)

    return await msg.answer(text=CategoryMessages(category).create_info_, reply_markup=sure2create_ikb())


@category_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_CATEGORY),
    CreateCategoryActions.ADD_CATEGORY_NAME,
    F.data == 'create'
)
async def create_category_handler(clb: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category: models.Category = state_data.get('category')

    if not category:
        logger.warning(f'State data has no category for user ({clb.from_user.id})')
        await clb.answer(_('Not found'))
        return

    category = await create_category(category)
    if not category:
        logger.warning(f'Category {category} is not created by user ({clb.from_user.id})')
        await clb.answer(_('Can not create'))
        return

    logger.info(f'User ({clb.from_user.id}) created category {category}')
    await clb.answer(_('Success'))
    await clb.message.delete()

    await state.clear()
