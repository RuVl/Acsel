from datetime import timedelta
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.fsm.storage.base import StorageKey
from sqlalchemy import select

from core.storages import get_storage
from database import session_maker
from database.models import User, UserRights


class DBUserMiddleware(BaseMiddleware):
    """ Get user from cache or database and check if user CAN_WRITE """

    def __init__(self, prefix='user_rights', cache_expire=timedelta(minutes=1), key='user', middleware_key='db_user') -> None:
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
        chat = event.message.chat if isinstance(event, types.CallbackQuery) else event.chat
        tg_user = event.from_user

        # Create fsm storage key
        key = StorageKey(
            bot_id=event.bot,
            chat_id=chat.id,
            user_id=tg_user.id
        )

        # Get cached user
        storage_data = await self.storage.get_data(key=key)
        user = storage_data.get(self.key)

        # If no cached user - get it from db
        if user is None:
            async with session_maker() as session:
                query = select(User).where(User.id == event.user_id)
                result = await session.execute(query)
                user = result.scalar()

                # If no user found - create it
                if user is None:
                    user = User(telegram_id=tg_user.id, username=tg_user.username)
                    session.add(user)

                    await session.commit()
                    await session.refresh(user)

            # update cache
            storage_data[self.key] = user
            await self.storage.set_data(key=key, data=user)

        # Provide db_user to handler and call it if the user is not BANNED
        if user.rights & UserRights.CAN_WRITE:
            data[self.middleware_key] = user
            return await handler(event, data)

    async def close(self) -> None:
        await self.storage.close()
