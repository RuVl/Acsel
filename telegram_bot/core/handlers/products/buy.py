import logging

from aiogram import Router, F
from aiogram.filters import MagicData, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.i18n import gettext as _
from sqlalchemy import Sequence

from core.keyboards.inline import choose_product_ikb, sure2buy_ikb, choose_quantity_ikb
from core.keyboards.inline.products import choose_category2buy_ikb, make_payment_ikb
from core.state_machines import BuyProductActions
from core.text.handlers import CommonMessages, ProductMessages
from database import session_maker
from database.enums import UserRights, TransactionStatuses
from database.methods.product import get_product
from database.methods.product_file import get_available_product_files, get_transaction_product_files
from database.methods.transaction import create_transaction, get_transaction
from database.models import Transaction, User
from database.utils import str2int
from database.validators import validate_product_quantity
from plisio import create_invoice, PlisioException

buy_router = Router()

logger = logging.getLogger('telegram')


@buy_router.message(
    MagicData(F.db_user.rights & UserRights.CAN_BUY),
    BuyProductActions.CHOSE_QUANTITY,
    F.text.isdecimal(),
    flags={'dialog': f'selected quantity'}
)
async def get_quantity_handler(msg: Message, state: FSMContext, state_data: dict) -> Message:
    quantity, = str2int(msg.text)

    state_product, category = state_data.get('product'), state_data.get('category')
    if state_product is None:
        await msg.reply(_('Not found'))
        return await return2product_select(msg, state, state_data)

    product = await get_product(state_product.id)
    if product is None:
        await msg.reply(_('All products are sold'))

    quantity = validate_product_quantity(quantity, product.quantity)
    if quantity is None:
        logger.debug(f'User {msg.from_user.id} passed invalid quantity {quantity} for product {product}')
        await msg.reply(_('Invalid quantity'))

        keyboard = await choose_quantity_ikb(product)
        return await msg.answer(ProductMessages(product, category).buy_info_, reply_markup=keyboard)

    await state.update_data(product=product, quantity=quantity)

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

    # Store user's quantity and get product category
    quantity = validate_product_quantity(quantity, product.quantity)
    if quantity is None:
        await clb.answer(_('Not enough products'))

        # If quantity was changed
        if state_product.quantity != product.quantity:
            keyboard = await choose_quantity_ikb(product)
            await clb.message.edit_text(ProductMessages(product, category).buy_info_, reply_markup=keyboard)

        return

    await clb.answer()
    await state.update_data(product=product, quantity=quantity)

    await state.set_state(BuyProductActions.SURE_TO_BUY)
    await clb.message.edit_text(ProductMessages(product, category).sure2buy_, reply_markup=sure2buy_ikb())


@buy_router.callback_query(
    MagicData(F.db_user.rights & UserRights.CAN_BUY),
    BuyProductActions.SURE_TO_BUY,
    F.data == 'buy'
)
async def sure2buy_handler(clb: CallbackQuery, state: FSMContext, db_user: User):
    state_data = await state.get_data()

    product_, category_, quantity_ = state_data.get('product'), state_data.get('category'), state_data.get('quantity')
    if product_ is None or category_ is None or quantity_ is None:
        logger.warning(f'State data has no product or category or quantity for user {clb.from_user.id}!')
        await clb.answer(_('Not found'))
        return

    async with session_maker() as session:
        product = await get_product(product_.id, session=session)
        if product is None:
            await clb.answer(_('All products are sold'))
            await return2product_select(clb, state, state_data)
            return

        # Validate quantity
        quantity = validate_product_quantity(quantity_, product.quantity)
        if quantity is None:
            await clb.answer(_('Not enough products'))
            await state.set_state(BuyProductActions.CHOSE_QUANTITY)
            keyboard = await choose_quantity_ikb(product)
            await clb.message.edit_text(ProductMessages(product, category_).buy_info_, reply_markup=keyboard)
            return

        total_price = product.price * quantity

        seq = Sequence('transactions_id_seq')
        next_id = await session.execute(seq)

        try:
            data = await create_invoice(
                order_name=f'User {db_user.telegram_id} buy {quantity} {product.name} from category {category_.name}', order_number=next_id,
                source_currency='USD', source_amount=total_price,
                expire_min=30
            )

            logger.info(f'Got response from plisio: {data}')
            txn_id = data['data']['txn_id']
            invoice_url = data['data']['invoice_url']
        except PlisioException as e:
            logger.error(str(e))
            await clb.answer(_('Something went wrong'))
            return

        files = await get_available_product_files(product, quantity, session=session)
        if len(files) != quantity:
            logger.warning(f'Can not get {quantity} product_files, got {len(files)} product_files')
            await clb.answer(_('Something went wrong'))
            return

        transaction = Transaction(
            id=next_id,
            total_price=total_price,
            quantity=quantity,
            user_id=db_user.id,
            txn_id=txn_id,
            files=files
        )

        logger.info(f'User ({db_user.telegram_id}) created transaction ({next_id}) - {txn_id}')
        transaction = await create_transaction(transaction, session=session)
        if transaction is None:
            logger.warning(f'Transaction ({next_id}) is not created for user {db_user.id}')
            await clb.answer(_('Transaction is not created'))
            return

    await state.update_data(transaction_id=transaction.id)
    await clb.answer()

    await state.set_state(BuyProductActions.CHECK_PAYMENT)
    await clb.message.edit_text(CommonMessages.make_payment, reply_markup=make_payment_ikb(invoice_url))


@buy_router.callback_query(
    BuyProductActions.CHECK_PAYMENT,
    F.data == 'check_payment'
)
async def check_payment_handler(clb: CallbackQuery, state: FSMContext, db_user: User):
    state_data = await state.get_data()
    transaction_id = state_data.get('transaction_id')
    if transaction_id is None:
        logger.warning(f'State has no transaction_id value')
        await clb.answer(_('Not found'))
        return

    transaction = await get_transaction(transaction_id)
    if transaction is None:
        logger.warning(f'No transaction with id {transaction_id} found')
        await clb.answer(_('Not found'))
        return

    if transaction.user_id != db_user.id:
        logger.warning(f'User {db_user.id} is not owner of transaction {transaction.id} (owner: {transaction.user_id})')
        await clb.answer(_('Something went wrong'))
        return

    logger.info(f'User ({db_user.telegram_id}) check transaction ({transaction.id}) status: {transaction.status}')

    if transaction.status in [TransactionStatuses.COMPLETED, TransactionStatuses.MISMATCH]:
        await clb.answer()
        await state.clear()

        await clb.message.edit_text(CommonMessages.thanks_for_purchase)

        logger.info(f'Send product files from transaction ({transaction.id}) to user ({db_user.id})')
        files = await get_transaction_product_files(transaction.id)
        for file in files:
            await clb.message.answer_document(FSInputFile(file.path))
        return

    if transaction.status in [TransactionStatuses.CANCELLED, TransactionStatuses.EXPIRED]:
        await clb.answer()
        await state.clear()

        if transaction.status == TransactionStatuses.EXPIRED:
            await clb.message.edit_text(CommonMessages.transaction_expired)
        elif transaction.status == TransactionStatuses.CANCELLED:
            await clb.message.edit_text(CommonMessages.transaction_cancelled)
        return

    await clb.answer(_('Wait for confirmation'))


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
