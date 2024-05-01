import logging

from aiogram import Router, F
from aiogram.filters import MagicData, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _

from core.keyboards.inline import choose_product_ikb, sure2buy_ikb, choose_quantity_ikb
from core.keyboards.inline.products import choose_category2buy_ikb
from core.state_machines import BuyProductActions
from core.text.handlers import CommonMessages, ProductMessages
from database.enums import UserRights
from database.methods.product import get_product
from database.utils import str2int

buy_router = Router()

logger = logging.getLogger('telegram')


@buy_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_BUY),
    BuyProductActions.CHOSE_QUANTITY,
    F.text.isdecimal(),
    flags={'dialog': f'selected quantity'}
)
async def select_quantity_handler(msg: Message, state: FSMContext, state_data: dict) -> Message:
    quantity, = str2int(msg.text)

    state_product, category = state_data.get('product'), state_data.get('category')
    if state_product is None:
        await msg.reply(_('Not found'))
        return await return2product_select(msg, state, state_data)

    product = await get_product(state_product.id)
    if product is None:
        await msg.reply(_('All products are sold'))

    try:
        product.quantity = quantity
    except ValueError:
        logger.warning(f'User {msg.from_user.id} passed invalid quantity {quantity} for product {product}')
        await msg.reply(_('Invalid quantity'))
        keyboard = await choose_quantity_ikb(product)
        return await msg.answer(ProductMessages(product, category).buy_info_, reply_markup=keyboard)

    await state.update_data(product=product)

    await state.set_state(BuyProductActions.SURE_TO_BUY)
    return await msg.answer(ProductMessages(product, category).sure2buy_, reply_markup=sure2buy_ikb())


@buy_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_BUY),
    BuyProductActions.CHOSE_QUANTITY,
    F.data.isdecimal() | F.data == 'back'
)
async def select_quantity_handler(clb: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if clb.data == 'back':
        await clb.answer()
        await return2product_select(clb, state, state_data)
        return

    quantity, = str2int(clb.data)
    state_product, category = state_data.get('product'), state_data.get('category')

    if state_product is None or category is None:
        logger.warning(f'State data has no product or category for user {clb.from_user.id}!')
        await clb.answer(_('Not found'))
        return

    # Update from db
    product = await get_product(state_product.id)
    if product is None:
        await clb.answer(_('All products are sold'))
        await return2product_select(clb, state, state_data)
        return

    if product.quantity > quantity:
        await clb.answer(_('Not enough products'))
        return

    # Store user's quantity and get product category
    try:
        product.user_quantity = quantity
    except ValueError:
        await clb.answer(_('Not enough products'))

        # If quantity was changed
        if state_product.quantity != product.quantity:
            await clb.message.edit_text(ProductMessages(product, category).buy_info_, reply_markup=sure2buy_ikb())

        return

    await clb.answer()
    await state.update_data(product=product)

    await state.set_state(BuyProductActions.SURE_TO_BUY)
    await clb.message.edit_text(ProductMessages(product, category).sure2buy_, reply_markup=sure2buy_ikb())


@buy_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_BUY),
    BuyProductActions.SURE_TO_BUY,
    F.data == 'buy'
)
async def sure2buy_handler(clb: CallbackQuery, state: FSMContext):
    # TODO send request to plisio, store transaction and waiting for purchase
    pass


@buy_router.callback_query(
    or_f(*BuyProductActions.__all_states__),
    F.data == 'cancel',
    flags={'preserve_fsm': ''}
)
async def cancel_handler(clb: CallbackQuery, state: FSMContext):
    await clb.answer()
    await state.clear()
    await clb.message.delete()


# ===== Utils ======
async def return2product_select(msg_or_clb: Message | CallbackQuery, state: FSMContext, state_data: dict):
    send_msg = msg_or_clb.message.edit_text if isinstance(msg_or_clb, CallbackQuery) else msg_or_clb.answer
    category = state_data.get('category')

    # If no category found return to category select
    if category is None:
        logger.warning(f'State data has no category for user {msg_or_clb.from_user.id}!')
        await state.set_state(BuyProductActions.SELECT_CATEGORY)

        keyboard = await choose_category2buy_ikb()
        return await send_msg(CommonMessages.choose_category, reply_markup=keyboard)

    await state.set_state(BuyProductActions.SELECT_PRODUCT)

    keyboard = await choose_product_ikb(category)
    return await send_msg(CommonMessages.choose_product, reply_markup=keyboard)
