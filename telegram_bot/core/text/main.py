from pathlib import Path

from aiogram.utils.i18n import I18n

locales_path = Path(__file__).parent / 'locales'

i18n = I18n(path=locales_path, default_locale='en', domain='messages')
