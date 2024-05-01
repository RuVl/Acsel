import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from aiogram import types

from database import models


class TGEncoder(json.JSONEncoder):
    """ Write encoder for all you need in state.set_data """

    def __init__(self, *args: Any, **kwargs: Any):
        self.visited = set()
        super().__init__(*args, **kwargs)

    def default(self, o: Any) -> Any:
        if isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, Path):  # pathlib.Path
            return {
                "_type": f'{o.__module__}.{type(o).__name__}',
                "_value": str(o.absolute())
            }
        elif isinstance(o, datetime):  # datetime.datetime
            return {
                "_type": 'datetime.datetime',
                "_value": o.isoformat()
            }
        elif isinstance(o, types.TelegramObject):  # aiogram.types
            return {
                "_type": f'{o.__module__}.{type(o).__name__}',
                "_value": {k: v for k, v in o.__dict__.items() if v is not None}
            }
        elif isinstance(o, models.Base):  # database.models
            self.visited.add(hash(o))

            # Add attributes to dict and check if wasn't circular references
            _value = {
                k: v if not isinstance(v, list) else filter(lambda i: hash(i) not in self.visited, v)
                for k, v in o.__dict__.items()
                if v is not None
            }

            _value.pop('_sa_instance_state', None)
            return {
                "_type": f'{o.__module__}.{type(o).__name__}',
                "_value": _value
            }

        return super(TGEncoder, self).default(o)
