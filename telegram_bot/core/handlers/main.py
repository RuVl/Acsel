from aiogram import Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware

from core.handlers.products import products_router
from core.middlewares import DBUserMiddleware
from core.text import i18n


def register_middlewares(dp: Dispatcher):
    # db_user middleware
    db_user_middleware = DBUserMiddleware()

    # Outer middleware for early dropping event
    dp.message.outer_middleware(db_user_middleware)
    dp.callback_query.outer_middleware(db_user_middleware)

    dp.shutdown.register(db_user_middleware.close)

    # i18n middleware (message and callback)
    i18n_middleware = FSMI18nMiddleware(i18n, key='lang', middleware_key='language')

    # Outer middleware for support filtering
    dp.message.outer_middleware(i18n_middleware)
    dp.callback_query.outer_middleware(i18n_middleware)


def register_routers(dp: Dispatcher):
    dp.include_routers(products_router)


def register_all(dp: Dispatcher):
    register_routers(dp)
    register_middlewares(dp)
