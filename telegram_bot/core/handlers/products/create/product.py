import logging

from aiogram import Router, F
from aiogram.filters import MagicData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from core.keyboards.inline import sure2create_ikb, cancel_ikb, choose_category_ikb, skip_or_cancel_ikb
from core.state_machines import CreateProductActions
from core.text.handlers import PrivilegeMessages, ProductMessages
from core.text.keyboards import MainMenuCKbMessages
from database import models
from database.enums import UserRights
from database.methods.product import create_product
from database.validators import validate_product_name, validate_product_price, validate_product_description

product_router = Router()

logger = logging.getLogger('telegram')


@product_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    F.text == MainMenuCKbMessages.add_product,
    flags={'dialog': 'choose a category for a new product'}
)
async def add_product_handler(msg: Message, state: FSMContext) -> Message:
    await state.clear()
    await state.set_state(CreateProductActions.SELECT_CATEGORY)
    keyboard = await choose_category_ikb()
    return await msg.answer(text=PrivilegeMessages.select_category, reply_markup=keyboard)


@product_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    F.text.not_in(MainMenuCKbMessages.all_replies()),
    CreateProductActions.ADD_PRODUCT_NAME,
    flags={'dialog': 'added product name'}
)
async def add_product_name_handler(msg: Message, state: FSMContext, state_data: dict) -> Message:
    name = validate_product_name(msg.text)
    if not name:
        logger.warning(f'User ({msg.from_user.id}) tried to set invalid product name: {msg.text}')
        return await msg.reply(PrivilegeMessages.invalid_product_name)

    category: models.Product = state_data.get('category')

    if category is None:
        logger.warning(f'State data has no category for user {msg.from_user.id}!')
        return await msg.reply(_('Not found'))

    product = models.Product(category_id=category.id, name=name)
    logger.debug(f'User ({msg.from_user.id}) set product name {product}')
    await state.update_data(product=product)

    await state.set_state(CreateProductActions.ADD_PRODUCT_DESCRIPTION)
    return await msg.answer(text=PrivilegeMessages.ask_product_description, reply_markup=skip_or_cancel_ikb())


@product_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    F.text.not_in(MainMenuCKbMessages.all_replies()),
    CreateProductActions.ADD_PRODUCT_DESCRIPTION,
    flags={'dialog': 'added product description'}
)
async def add_product_description_handler(msg: Message, state: FSMContext, state_data: dict) -> Message:
    description = validate_product_description(msg.text)
    if not description:
        logger.warning(f'User ({msg.from_user.id}) tried to set invalid product description: {msg.text}')
        return await msg.reply(PrivilegeMessages.invalid_product_description)

    product: models.Product = state_data.get('product')

    if product is None:
        logger.warning(f'State data has no product for user {msg.from_user.id}!')
        return await msg.reply(_('Not found'))

    product.description = description
    logger.debug(f'User ({msg.from_user.id}) set product description {product}')
    await state.update_data(product=product)

    await state.set_state(CreateProductActions.ADD_PRODUCT_PRICE)
    return await msg.answer(text=PrivilegeMessages.ask_product_price, reply_markup=cancel_ikb())


@product_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    CreateProductActions.ADD_PRODUCT_DESCRIPTION,
    F.data == 'skip'
)
async def skip_product_description_handler(clb: CallbackQuery, state: FSMContext):
    logger.debug(f'User ({clb.from_user.id}) skipped setting product description')
    await clb.answer()
    await state.set_state(CreateProductActions.ADD_PRODUCT_PRICE)
    await clb.message.edit_text(PrivilegeMessages.ask_product_price, reply_markup=cancel_ikb())


@product_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    F.text.not_in(MainMenuCKbMessages.all_replies()),
    CreateProductActions.ADD_PRODUCT_PRICE,
    flags={'dialog': 'added product price'}
)
async def add_product_price_handler(msg: Message, state: FSMContext, state_data: dict) -> Message:
    price = validate_product_price(msg.text)
    if not price:
        logger.warning(f'User ({msg.from_user.id}) tried to set invalid product price: {msg.text}')
        return await msg.reply(text=PrivilegeMessages.invalid_product_price)

    product: models.Product = state_data.get('product')
    category: models.Category = state_data.get('category')

    if product is None or category is None:
        logger.warning(f'State data has no product or category for user {msg.from_user.id}!')
        return await msg.reply(_('Not found'))

    product.price = price
    logger.debug(f'User ({msg.from_user.id}) set product price {product}')
    await state.update_data(product=product)

    await state.set_state(CreateProductActions.SURE_CREATE_PRODUCT)
    return await msg.answer(text=ProductMessages(product, category).create_info_, reply_markup=sure2create_ikb())


@product_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
    CreateProductActions.SURE_CREATE_PRODUCT,
    F.data == 'create'
)
async def create_product_handler(clb: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    product: models.Product = state_data.get('product')

    if product is None:
        logger.warning(f'State data has no product for user {clb.from_user.id}!')
        await clb.answer(_('Not found'))
        return

    product = await create_product(product)
    if not product:
        logger.warning(f'Product {product} is not created by user ({clb.from_user.id})')
        await clb.answer(_('Can not create'))
        return

    logger.info(f'User ({clb.from_user.id}) created product {product}')
    await clb.answer(_('Success'))

    await clb.message.delete()
    await state.clear()
