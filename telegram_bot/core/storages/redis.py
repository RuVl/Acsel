import json
from datetime import timedelta

from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis

from core.env import RedisKeys
from . import TGDecoder, TGEncoder


def get_storage(*,
                state_ttl: timedelta | int | None = None,
                data_ttl: timedelta | int | None = None,
                key_builder_prefix: str = 'fsm',
                key_builder_separator: str = ':',
                key_builder_with_bot_id: bool = False,
                key_builder_with_destiny: bool = False,
                ) -> BaseStorage:
    return RedisStorage(
        Redis.from_url(RedisKeys.URL),
        key_builder=DefaultKeyBuilder(
            prefix=key_builder_prefix,
            separator=key_builder_separator,
            with_bot_id=key_builder_with_bot_id,
            with_destiny=key_builder_with_destiny
        ),
        state_ttl=state_ttl,
        data_ttl=data_ttl,
        json_dumps=lambda data: json.dumps(data, cls=TGEncoder),
        json_loads=lambda data: json.loads(data, cls=TGDecoder)
    )
