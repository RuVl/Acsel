from aiogram.filters.callback_data import CallbackData


class PaginatorFactory(CallbackData, prefix='paginator'):
    menu: str
    action: str
    page: int


class CategoryFactory(CallbackData, prefix='category'):
    id: int
    name: str


class ProductFactory(CallbackData, prefix='product'):
    id: int
    name: str
