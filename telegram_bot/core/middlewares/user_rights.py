from datetime import timedelta
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler
from aiogram.fsm.storage.base import StorageKey

from core.storages import get_storage
from database.enums import UserRights
from database.methods.user import get_user, create_user
from database.models import User


class DBUserMiddleware(BaseMiddleware):
    """ Get user from cache or database and check if user CAN_WRITE """

    def __init__(self, prefix='user_info', cache_expire=timedelta(minutes=1), key='user', middleware_key='db_user') -> None:
        # Get storage with prefix and set data ttl
        self.storage = get_storage(key_builder_prefix=prefix, data_ttl=cache_expire)

        self.key = key
        self.middleware_key = middleware_key

        super(DBUserMiddleware, self).__init__()

    async def __call__(self,
                       handler: Callable[[types.CallbackQuery | types.Message, dict[str, Any]], Awaitable[Any]],
                       event: types.CallbackQuery | types.Message,
                       data: dict[str, Any],
                       ) -> Any:
        chat: types.Chat = event.message.chat if isinstance(event, types.CallbackQuery) else event.chat
        tg_user: types.User = event.from_user

        # Create a storage key
        key = StorageKey(
            bot_id=event.bot,
            chat_id=chat.id,
            user_id=tg_user.id
        )

        # Get cached user
        storage_data = await self.storage.get_data(key=key)
        user: User = storage_data.get(self.key)

        # If no cached user - get it from db
        if user is None:
            # get or create a new user in db
            user = await get_user(tg_user.id)
            if user is None:
                user = create_user(tg_user)

            # update cached user
            storage_data[self.key] = user
            await self.storage.set_data(key=key, data=storage_data)

        # Provide db_user to handler and call it if the user is not BANNED
        if user.rights != UserRights.BANNED:
            data[self.middleware_key] = user
            return await handler(event, data)

        return CancelHandler()

    async def close(self) -> None:
        await self.storage.close()
