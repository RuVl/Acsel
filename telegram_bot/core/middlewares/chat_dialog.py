import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.flags import get_flag
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext


class ChatDialogMiddleware(BaseMiddleware):
    """ Store and deletes last dialog message. Works with USER_IN_CHAT fsm strategy """

    def __init__(self, /,
                 flag_name: str = 'dialog', fsm_key: str = 'last_msg_id',
                 logger_name: str = 'telegram'):
        self.flag_name = flag_name
        self.fsm_key = fsm_key
        self.logger = logging.getLogger(logger_name)

        super().__init__()

    async def __call__(self,
                       handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
                       event: types.Message,
                       data: dict[str, Any],
                       ) -> Any:
        description: str = get_flag(data, self.flag_name)
        if description is None:
            return await handler(event, data)

        # Use fsm storage
        state: FSMContext = data['state']
        state_data = await state.get_data()

        # Delete last dialog message (must be in this chat)
        last_msg_id: int = state_data.pop(self.fsm_key, None)
        if last_msg_id is not None:
            try:
                await event.bot.delete_message(event.chat.id, last_msg_id)
            except TelegramBadRequest as e:
                self.logger.error(f'Failed to delete dialog message {last_msg_id} in chat {event.chat.id} - {e.message}')

        data['state_data'] = state_data
        result = await handler(event, data)

        if isinstance(result, types.Message):
            await state.update_data({self.fsm_key: result.message_id})

            if description.strip():
                self.logger.info(f'User ({event.from_user.id}) {description}')

        return result
