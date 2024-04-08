from os import environ
from typing import Final


class PostgresKeys:
    USER: Final[str] = environ.get('POSTGRES_USER', default='postgres')
    PASSWORD: Final[str] = environ.get('POSTGRES_PASSWORD', default='')

    HOST: Final[str] = environ.get('POSTGRES_HOST', default='localhost')
    PORT: Final[str] = environ.get('POSTGRES_PORT', default='5432')

    DATABASE: Final[str] = environ.get('POSTGRES_DB', default=USER)

    URL: Final[str] = f'postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'