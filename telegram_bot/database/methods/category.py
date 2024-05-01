from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Category
from database.utils import str2int
from .utils import optional_session


@optional_session
async def create_category(category: Category, /, session: AsyncSession) -> Category | None:
    session.add(category)

    await session.commit()
    await session.refresh(category)

    return category


@optional_session
async def get_all_categories(session: AsyncSession) -> list[Category]:
    query = select(Category)
    result = await session.scalars(query)
    return result.all()


@optional_session
async def get_categories2buy(session: AsyncSession) -> list[Category]:
    query = select(Category).filter(Category.total_products > 0)
    result = await session.scalars(query)
    return result.all()


@optional_session
async def get_category(category_id: int | str, session: AsyncSession) -> Category | None:
    category_id, = str2int(category_id)
    query = select(Category).where(Category.id == category_id)
    return await session.scalar(query)
