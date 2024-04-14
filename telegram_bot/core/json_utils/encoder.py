import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from aiogram import types

from database import models


class TGEncoder(json.JSONEncoder):
    """ Write encoder for all you need in state.set_data """

    def default(self, o: Any) -> Any:
        if isinstance(o, Path):  # pathlib.Path
            return {
                "_module": o.__module__,
                "_type": type(o).__name__,
                "_value": str(o.absolute())
            }
        elif isinstance(o, datetime):  # datetime.datetime
            return {
                "_module": o.__module__,
                "_type": type(o).__name__,
                "_value": o.isoformat()
            }
        elif isinstance(o, types.TelegramObject):  # aiogram.types
            return {
                "_module": o.__module__,
                "_type": type(o).__name__,
                "_value": {k: v for k, v in o.__dict__.items() if v is not None}
            }
        elif isinstance(o, models.Base):  # database.models
            _value = {k: v for k, v in o.__dict__.items() if v is not None}
            _value.pop('_sa_instance_state', None)
            return {
                "_module": o.__module__,
                "_type": type(o).__name__,
                "_value": _value
            }

        logging.warning(f"Cannot serialize {o}")
        return super(TGEncoder, self).default(o)
