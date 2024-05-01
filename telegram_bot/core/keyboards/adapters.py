from aiogram.types import InlineKeyboardButton

from core.keyboards.callback_factories import CategoryFactory, ProductFactory
from database.models import Category, Product


def category2keyboard(category: Category) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=str(category),
        callback_data=CategoryFactory(id=category.id, name=category.name).pack(),
    )


def product2keyboard(product: Product) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=str(product),
        callback_data=ProductFactory(id=product.id, name=product.name).pack(),
    )
