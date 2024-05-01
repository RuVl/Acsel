from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler


class DropEmptyButtonMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[types.CallbackQuery, dict[str, Any]], Awaitable[Any]],
                       event: types.CallbackQuery,
                       data: dict[str, Any],
                       ) -> Any:
        if event.data == 'empty_button':
            await event.answer()
            return CancelHandler()

        return await handler(event, data)
