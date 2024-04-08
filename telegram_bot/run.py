import logging
import uvloop
from core import start_bot


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    uvloop.run(start_bot())
