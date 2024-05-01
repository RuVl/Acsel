import logging
import tempfile
from pathlib import Path

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from core.keyboards.inline import cancel_ikb, choose_category_ikb
from core.state_machines import CreateFileActions
from core.text.handlers import PrivilegeMessages
from core.text.keyboards import MainMenuCKbMessages
from database import models
from database.enums import UserRights
from database.methods.product_file import create_product_file_by_temp_path

file_router = Router()

logger = logging.getLogger('telegram')


@file_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_FILE),
    F.text == MainMenuCKbMessages.add_product_files,
    flags={'dialog': 'choose category for a new product file', 'preserve_fsm': ''}
)
async def add_product_file_handler(msg: Message, state: FSMContext) -> Message:
    await state.clear()
    await state.set_state(CreateFileActions.SELECT_CATEGORY)
    keyboard = await choose_category_ikb()
    return await msg.answer(text=PrivilegeMessages.select_category, reply_markup=keyboard)


@file_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_FILE),
    F.content_type == ContentType.DOCUMENT,
    CreateFileActions.ADD_PRODUCT_FILES,
    flags={'dialog': 'created a new product file'}
)
async def add_product_files_handler(msg: Message, state_data: dict) -> Message:
    product: models.Product = state_data.get('product')

    if product is None:
        logger.warning(f'State data has no product for user {msg.from_user.id}!')
        await msg.reply(_('Not found'))
        return

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        file_name = Path(msg.document.file_name)
        if not file_name.suffix:
            logger.warning(f'Can not define file extension {msg.document.file_name} from user {msg.from_user.id}!')

        document_path = Path(tmp_dir) / (msg.document.file_unique_id + file_name.suffix)
        await msg.bot.download(msg.document, document_path)

        if not document_path.exists():
            logger.warning(f'Downloading file {msg.document.file_name} failed from user {msg.from_user.id}!')
            await msg.reply(PrivilegeMessages.download_file_error)
            return

        logger.debug(f'File downloaded {document_path.name} from user {msg.from_user.id}')

        product_file = await create_product_file_by_temp_path(document_path, product.id)
        if not product_file:
            logger.warning(f'Product file {product_file} is not created by user ({msg.from_user.id})')
            await msg.reply(_('Can not create'))
            return

        logger.info(f'User ({msg.from_user.id}) created product file {product_file}')

    await msg.reply(PrivilegeMessages.success_add_product_file, reply_markup=cancel_ikb(_('Back')))
    return
