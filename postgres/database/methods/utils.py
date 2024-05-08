import functools
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from database import session_maker


def optional_session(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        if session is None or not isinstance(session, AsyncSession):
            async with session_maker() as session:
                kwargs['session'] = session
                return await func(*args, **kwargs)

        return await func(*args, **kwargs)

    return wrapper
