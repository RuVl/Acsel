from os import environ
from typing import Final


class PlisioKeys:
    API_TOKEN: Final[str] = environ.get('PLISIO_API_TOKEN')
