import logging
from pathlib import Path

from fastapi import FastAPI

from api.routers import plisio

description = """
Acsel API is temporary useless.
It only listen updates from plisio and update transaction status.
"""

tags_metadata = [
    {
        "name": "plisio",
        "description": "Listen updates from plisio",
    }
]

app = FastAPI(
    title="Acsel API",
    description=description,
    version="0.0.1",
    contact={
        "name": "RuVl",
        "url": "https://github.com/RuVl",
        "email": "vlad5050505@gmail.com",
    },
    license_info={
        "name": "GNU General Public License Version 3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
        "identifier": "GPL-3.0",
    },
    openapi_tags=tags_metadata,
    root_path='/api'
)
app.include_router(plisio.router)


def setup_loggers():
    LOGGING_FOLDER = Path('logging/')
    LOGGING_FOLDER.mkdir(exist_ok=True)

    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

    # telegram logger
    plisio_logger = logging.getLogger('plisio')
    plisio_logger.setLevel(logging.DEBUG)

    plisio_file_handler = logging.FileHandler(LOGGING_FOLDER / 'plisio.log')
    plisio_file_handler.setLevel(logging.DEBUG)
    plisio_file_handler.setFormatter(FORMATTER)

    plisio_logger.addHandler(plisio_file_handler)


if __name__ == '__main__':
    setup_loggers()
