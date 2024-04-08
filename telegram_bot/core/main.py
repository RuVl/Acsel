from aiogram import Dispatcher

from core import bot
from core.handlers import register_all, set_default_commands
from core.storages import get_storage


async def start_bot():
    dp = Dispatcher(storage=get_storage())

    register_all(dp)
    await set_default_commands(bot)

    # await core.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
