from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.flags import get_flag


class PreserveFSMKeysMiddleware(BaseMiddleware):
    """ Protect fsm keys against deletion (allow change value) """

    def __init__(self, /,
                 flag_name: str = 'preserve_fsm', sep: str = ',',
                 default_preserve_keys: tuple[str] | str = 'locale'):
        self.flag_name = flag_name
        self.sep = sep
        self.default_preserve_keys = self.parse_preserve_keys(default_preserve_keys, False)

        super().__init__()

    def parse_preserve_keys(self, preserve: str | list | tuple, use_default=True) -> list[str] | tuple[str]:
        preserve_keys = self.default_preserve_keys if use_default else None
        if isinstance(preserve, tuple | list):
            preserve_keys = preserve
        elif isinstance(preserve, str) and preserve.strip():
            preserve_keys = preserve.split(self.sep)
        return preserve_keys

    async def __call__(self,
                       handler: Callable[[types.CallbackQuery | types.Message, dict[str, Any]], Awaitable[Any]],
                       event: types.TelegramObject,
                       data: dict[str, Any],
                       ) -> Any:

        preserve: str | list | tuple = get_flag(data, self.flag_name)
        if preserve is None:  # If no flag provided - skip preserving
            return await handler(event, data)
        preserve_keys = self.parse_preserve_keys(preserve)

        # Get current state_data
        state, state_data = data.get('state'), data.get('state_data')
        if state_data is None:
            state_data = await state.get_data()

        result = await handler(event, data)

        # Set default previous keys to new_state_data
        new_state_data = await state.get_data()
        for key in preserve_keys:
            new_state_data.setdefault(key, state_data.get(key))

        await state.set_data(new_state_data)
        return result
