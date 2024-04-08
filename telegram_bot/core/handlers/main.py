from aiogram import Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware

from core.handlers.user import user_router
from core.text import i18n


def register_middlewares(dp: Dispatcher):
    # i18n middleware (message and callback)
    i18n_middleware = FSMI18nMiddleware(i18n, key='lang', middleware_key='language')

    # Outer middleware for support filtering
    dp.message.outer_middleware(i18n_middleware)
    dp.callback_query.outer_middleware(i18n_middleware)


def register_routers(dp: Dispatcher):
    # User router
    dp.include_router(user_router)


def register_all(dp: Dispatcher):
    register_routers(dp)
    register_middlewares(dp)
