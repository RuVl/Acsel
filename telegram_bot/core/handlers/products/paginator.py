import logging

from aiogram import Router, F
from aiogram.filters import and_f, MagicData, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from core.keyboards.callback_factories import CategoryFactory, PaginatorFactory, ProductFactory
from core.keyboards.inline import choose_product_ikb, cancel_ikb, choose_category_ikb, choose_quantity_ikb
from core.keyboards.inline.products import choose_product2buy_ikb, choose_category2buy_ikb
from core.state_machines import CreateProductActions, CreateFileActions, BuyProductActions
from core.text.handlers import PrivilegeMessages, CommonMessages, ProductMessages
from database.enums import UserRights
from database.methods.category import get_category
from database.methods.product import get_product

paginator_router = Router()

logger = logging.getLogger('telegram')


@paginator_router.callback_query(
    or_f(
        and_f(
            MagicData(F.db_user.rights & UserRights.CAN_ADD_PRODUCT),
            CreateProductActions.SELECT_CATEGORY
        ),
        and_f(
            MagicData(F.db_user.rights & UserRights.CAN_ADD_FILE),
            CreateFileActions.SELECT_CATEGORY,
        ),
        and_f(
            MagicData(F.db_user.rights & UserRights.CAN_BUY),
            BuyProductActions.SELECT_CATEGORY
        )
    ),
    CategoryFactory.filter()
)
async def select_category_handler(clb: CallbackQuery, callback_data: CategoryFactory, state: FSMContext):
    # Get category by id from db
    category = await get_category(callback_data.id)

    # Check if category has found
    if category is None:
        logger.warning(f"User's ({clb.from_user.id}) callback_data (CategoryFactory) has wrong id={callback_data.id}!")
        await clb.answer(_('Not found'))
        return

    # Additional validation check
    if category.name != callback_data.name:
        logger.warning(f"User's ({clb.from_user.id}) category name {category} is not equals to callback_data.name={callback_data.name}!")
        await clb.answer(_('Not found'))
        return

    logger.debug(f'User ({clb.from_user.id}) selected category {category}')

    await clb.answer()
    await state.update_data(category=category)  # store category in fsm data

    # Choose data according state
    match await state.get_state():
        case CreateProductActions.SELECT_CATEGORY:
            text = PrivilegeMessages.ask_product_name
            keyboard = cancel_ikb()
            action = CreateProductActions.ADD_PRODUCT_NAME
        case CreateFileActions.SELECT_CATEGORY:
            text = PrivilegeMessages.select_product
            keyboard = await choose_product_ikb(category)
            action = CreateFileActions.SELECT_PRODUCT
        case BuyProductActions.SELECT_CATEGORY:
            text = CommonMessages.choose_product
            keyboard = await choose_product2buy_ikb(category)
            action = BuyProductActions.SELECT_PRODUCT
        case _:
            raise NotImplementedError()

    # Update message for next step
    await state.set_state(action)
    await clb.message.edit_text(text, reply_markup=keyboard)


@paginator_router.callback_query(
    or_f(
        CreateProductActions.SELECT_CATEGORY,
        CreateFileActions.SELECT_CATEGORY,
        BuyProductActions.SELECT_CATEGORY
    ),
    PaginatorFactory.filter(F.action == 'change_page')
)
async def change_category_page_handler(clb: CallbackQuery, callback_data: PaginatorFactory, state: FSMContext):
    await clb.answer()

    match await state.get_state():
        case CreateProductActions.SELECT_CATEGORY | CreateFileActions.SELECT_CATEGORY:
            keyboard = await choose_category_ikb(page=callback_data.page)
        case BuyProductActions.SELECT_CATEGORY:
            keyboard = choose_category2buy_ikb(page=callback_data.page)

    await clb.message.edit_reply_markup(reply_markup=keyboard)


@paginator_router.callback_query(
    or_f(
        and_f(
            MagicData(F.db_user.rights & UserRights.CAN_ADD_FILE),
            CreateFileActions.SELECT_PRODUCT,
        ),
        and_f(
            MagicData(F.db_user.rights & UserRights.CAN_BUY),
            BuyProductActions.SELECT_PRODUCT
        )
    ),
    ProductFactory.filter()
)
async def select_product_handler(clb: CallbackQuery, callback_data: ProductFactory, state: FSMContext, state_data: dict):
    # Get product by id from db
    product = await get_product(callback_data.id)

    # Check if product has found
    if product is None:
        logger.warning(f"User's ({clb.from_user.id}) callback_data (ProductFactory) has wrong id={callback_data.id}!")
        await clb.answer(_('Not found'))
        return

    # Additional validation check
    if product.name != callback_data.name:
        logger.warning(f"User's ({clb.from_user.id}) product name {product} is not equals to callback_data.name={callback_data.name}!")
        await clb.answer(_('Not found'))
        return

    logger.debug(f'User ({clb.from_user.id}) selected product {product}')

    await clb.answer()
    await state.update_data(product=product)  # store category in fsm data

    # Choose data according state
    match await state.get_state():
        case CreateFileActions.SELECT_PRODUCT:
            text = PrivilegeMessages.ask_product_files
            keyboard = cancel_ikb()
            action = CreateFileActions.ADD_PRODUCT_FILES
        case BuyProductActions.SELECT_PRODUCT:
            category = state_data.get('category')

            if category is None:
                logger.warning(f'State data has no category for user {clb.from_user.id}!')
                await clb.answer(_('Not found'))
                return

            text = ProductMessages(product, category).buy_info_
            keyboard = await choose_quantity_ikb(product)
            action = BuyProductActions.CHOSE_QUANTITY
        case _:
            raise NotImplementedError()

    # Update message for next step
    await state.set_state(action)
    await clb.message.edit_text(text, reply_markup=keyboard)


@paginator_router.callback_query(
    or_f(
        CreateFileActions.SELECT_PRODUCT,
        BuyProductActions.SELECT_PRODUCT
    ),
    PaginatorFactory.filter(F.action == 'change_page')
)
async def change_product_page_handler(clb: CallbackQuery, callback_data: PaginatorFactory, state: FSMContext):
    state_data = await state.get_data()
    category = state_data.get('category')

    if category is None:
        logger.warning(f'State data has no category for user {clb.from_user.id}!')
        await clb.answer(_('Not found'))
        return

    await clb.answer()

    match await state.get_state():
        case CreateFileActions.SELECT_PRODUCT:
            keyboard = await choose_product_ikb(category, page=callback_data.page)
        case BuyProductActions.SELECT_PRODUCT:
            keyboard = choose_product2buy_ikb(category, page=callback_data.page)

    await clb.message.edit_reply_markup(reply_markup=keyboard)
