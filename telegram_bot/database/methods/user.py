from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.utils import str2int
from .utils import optional_session


@optional_session
async def get_user(tg_id: int | str, /, session: AsyncSession) -> User:
    tg_id, = str2int(tg_id)
    query = select(User).where(User.telegram_id == tg_id)
    return await session.scalar(query)


@optional_session
async def create_user(tg_user: User, /, session: AsyncSession) -> User:
    user = User(telegram_id=tg_user.id, username=tg_user.username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
