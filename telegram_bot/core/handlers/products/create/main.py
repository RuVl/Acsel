import logging

from aiogram import Router, F, types
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext

from core.state_machines import CreateCategoryActions, CreateProductActions, CreateFileActions
from .category import category_router
from .product import product_router
from .product_file import file_router

create_router = Router()
create_router.include_routers(category_router, product_router, file_router)

logger = logging.getLogger('telegram')


# === Shared ===
@create_router.callback_query(
    or_f(
        *CreateCategoryActions.__all_states__,
        *CreateProductActions.__all_states__,
        *CreateFileActions.__all_states__
    ),
    F.data == 'cancel',
    flags={'preserve_fsm': ''}
)
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.delete()
