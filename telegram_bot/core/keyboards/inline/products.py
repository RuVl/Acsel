from math import log, floor, ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards.adapters import category2keyboard, product2keyboard
from core.keyboards.utils import paginate
from database.methods.category import get_all_categories, get_categories2buy
from database.methods.product import get_category_products, get_product, get_category_products2buy
from database.models import Category, Product


async def choose_category_ikb(*, page=0, categories: list[Category] = None) -> InlineKeyboardMarkup:
    """ Show categories """

    if categories is None:
        categories = await get_all_categories()

    builder = paginate(categories, page, category2keyboard, 'category_menu', 1, 8)
    return builder.as_markup()


async def choose_category2buy_ikb(*, page=0) -> InlineKeyboardMarkup:
    categories = await get_categories2buy()
    return await choose_category_ikb(page=page, categories=categories)


async def choose_product_ikb(category: Category | int = None, *, page=0, products: list[Product] = None) -> InlineKeyboardMarkup:
    """ Show products """

    if products is None:
        if category is None:
            raise ValueError('Provide category or products list!')

        products = await get_category_products(category.id if isinstance(category, Category) else category)

    builder = paginate(products, page, product2keyboard, 'product_menu', 2, 8)
    return builder.as_markup()


async def choose_product2buy_ikb(category: Category | int, *, page=0) -> InlineKeyboardMarkup:
    products = await get_category_products2buy(category.id)
    return await choose_product_ikb(products=products, page=page)


async def choose_quantity_ikb(product: Product | int = None, max_quantity=100) -> InlineKeyboardMarkup:
    """
        Add shortcut buttons for choosing quantity.
        :param product: Product or product id for max quantity
        :param max_quantity: Maximum quantity if product is not provided
    """

    MAX_IN_ROW = 6
    if isinstance(product, Product):
        MAX_QUANTITY = product.quantity
    elif isinstance(product, int):
        product = await get_product(product)
        MAX_QUANTITY = product.quantity
    else:
        MAX_QUANTITY = max_quantity

    def get_button_number(n: int) -> int:
        p = 1.5 * log(10 * MAX_QUANTITY, 10)
        f = ceil(MAX_QUANTITY * pow(n / MAX_IN_ROW, p))
        r = 1 if f < 5 else 5 if f < 50 else 50 if f < 500 else 100
        return r * floor(f / r)

    button_numbers = set(map(get_button_number, range(1, MAX_IN_ROW + 1)))

    quantities = [
        InlineKeyboardButton(text=number, callback_data=number)
        for number in map(str, button_numbers)
    ]

    builder = InlineKeyboardBuilder()
    builder.row(*quantities) \
        .row(InlineKeyboardButton(text='back', callback_data='back')) \
        .row(InlineKeyboardButton(text='cancel', callback_data='cancel'))

    return builder.as_markup()


def sure2create_ikb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=_('Create'), callback_data='create'),
        InlineKeyboardButton(text=_('Cancel'), callback_data='cancel'),
    )
    return builder.as_markup()


def sure2buy_ikb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=_('Buy'), callback_data='buy'),
        InlineKeyboardButton(text=_('Cancel'), callback_data='cancel'),
    )
    return builder.as_markup()


def skip_or_cancel_ikb(text: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=_('Skip'), callback_data='skip')) \
        .row(InlineKeyboardButton(text=text or _('Cancel'), callback_data='cancel'))
    return builder.as_markup()


def cancel_ikb(text: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=text or _('Cancel'), callback_data='cancel'))
    return builder.as_markup()


def make_payment_ikb(url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=_('Make payment'), url=url)) \
        .row(InlineKeyboardButton(text=_('Check payment'), callback_data='check_payment'))
    return builder.as_markup()
