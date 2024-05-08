import logging
from pathlib import Path

from fastapi import FastAPI

from api.routers import plisio

app = FastAPI(root_path='/api')
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
