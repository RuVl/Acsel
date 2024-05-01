import logging
from pathlib import Path

from aiogram import Dispatcher

from core import bot
from core.handlers import register_all, set_default_commands
from core.storages import get_storage


def setup_loggers():
    LOGGING_FOLDER = Path('logging/')
    LOGGING_FOLDER.mkdir(exist_ok=True)

    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

    # telegram logger
    telegram_logger = logging.getLogger('telegram')
    telegram_logger.setLevel(logging.DEBUG)

    telegram_file_handler = logging.FileHandler(LOGGING_FOLDER / 'telegram.log')
    telegram_file_handler.setLevel(logging.DEBUG)
    telegram_file_handler.setFormatter(FORMATTER)

    telegram_logger.addHandler(telegram_file_handler)

    # json logger
    json_logger = logging.getLogger('json')
    json_logger.setLevel(logging.DEBUG)

    json_file_handler = logging.FileHandler(LOGGING_FOLDER / 'json.log')
    json_file_handler.setLevel(logging.DEBUG)
    json_file_handler.setFormatter(FORMATTER)

    json_logger.addHandler(json_file_handler)


async def start_bot():
    setup_loggers()

    dp = Dispatcher(storage=get_storage())

    register_all(dp)
    await set_default_commands(bot)

    # await core.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
