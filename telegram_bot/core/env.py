from os import environ
from typing import Final


class TelegramKeys:
    API_TOKEN: Final[str] = environ.get('TG_API_TOKEN')


class RedisKeys:
    HOST: Final[str] = environ.get('DOCKER_REDIS_HOST', default='localhost')
    PORT: Final[str] = environ.get('DOCKER_REDIS_PORT', default='6379')

    DATABASE: Final[str] = environ.get('REDIS_DB', default='0')

    URL: Final[str] = f'redis://{HOST}:{PORT}/{DATABASE}'
