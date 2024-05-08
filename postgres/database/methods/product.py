from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product
from database.utils import str2int
from .utils import optional_session


@optional_session
async def create_product(product: Product, /, session: AsyncSession) -> Product | None:
    session.add(product)

    await session.commit()
    await session.refresh(product)

    return product


@optional_session
async def get_category_products(category_id: int | str, session: AsyncSession) -> list[Product]:
    category_id, = str2int(category_id)
    query = select(Product).where(Product.category_id == category_id)

    result = await session.scalars(query)
    return result.all()


@optional_session
async def get_category_products2buy(category_id: int | str, session: AsyncSession) -> list[Product]:
    category_id, = str2int(category_id)
    query = select(Product).where(and_(Product.category_id == category_id, Product.quantity > 0))

    result = await session.scalars(query)
    return result.all()


@optional_session
async def get_product(product_id: int | str, session: AsyncSession) -> Product | None:
    product_id, = str2int(product_id)
    query = select(Product).where(Product.id == product_id)
    return await session.scalar(query)
