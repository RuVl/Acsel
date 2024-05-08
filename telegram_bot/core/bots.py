from aiogram import Bot
from aiogram.enums import ParseMode

from core.env import TelegramKeys

bot = Bot(token=TelegramKeys.API_TOKEN, parse_mode=ParseMode.MARKDOWN_V2)
