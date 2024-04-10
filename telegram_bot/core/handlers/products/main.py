from aiogram import Router

from core.handlers.products.common import common_router
from core.handlers.products.privilege import privilege_router

products_router = Router()
products_router.include_routers(privilege_router, common_router)
