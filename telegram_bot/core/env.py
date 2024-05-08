from os import environ
from pathlib import Path
from typing import Final


class MainKeys:
    PRODUCTS_FOLDER: Final[Path] = Path(environ.get('PRODUCTS_FOLDER')).resolve()


class TelegramKeys:
    API_TOKEN: Final[str] = environ.get('TG_API_TOKEN')


class RedisKeys:
    HOST: Final[str] = environ.get('REDIS_HOST', default='localhost')
    PORT: Final[str] = environ.get('REDIS_PORT', default='6379')

    DATABASE: Final[str] = environ.get('REDIS_DB', default='0')

    URL: Final[str] = f'redis://{HOST}:{PORT}/{DATABASE}'
