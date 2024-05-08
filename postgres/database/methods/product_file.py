from pathlib import Path
from shutil import copy2

from sqlalchemy import select, and_, asc
from sqlalchemy.ext.asyncio import AsyncSession

from core.env import MainKeys
from database.models import ProductFile, Product
from database.utils import str2int
from .category import get_category
from .product import get_product
from .utils import optional_session


@optional_session
async def create_product_file(product_file: ProductFile, /, session: AsyncSession) -> ProductFile | None:
    product = await get_product(product_file.product_id, session=session)
    if not product:
        return None

    category = await get_category(product.category_id, session=session)
    if not category:
        return None

    # Update quantity
    product.quantity += 1
    category.total_products += 1

    # Add product file
    session.add(product_file)

    await session.commit()
    await session.refresh(product_file)

    return product_file


@optional_session
async def create_product_file_by_temp_path(path: Path | str, product_id: int | str, session: AsyncSession) -> ProductFile | None:
    product_id, = str2int(product_id)
    path = copy2(path, MainKeys.PRODUCTS_FOLDER)

    product_file = ProductFile(path=path, product_id=product_id)
    return await create_product_file(product_file, session=session)


@optional_session
async def get_available_product_files(product: Product | int, quantity: int, /, session: AsyncSession) -> list[ProductFile]:
    product_id = product.id if isinstance(product, Product) else product

    query = select(ProductFile).where(
        and_(ProductFile.product_id == product_id, ProductFile.transaction_id is None)
    ).order_by(asc(ProductFile.id)).limit(quantity)

    result = await session.scalars(query)
    return result.all()


@optional_session
async def reserve_product_files(product_files: list[ProductFile], /, session: AsyncSession) -> list[ProductFile] | None:
    products = {}
    categories = {}

    for file in product_files:
        if file.product_id not in products:
            product = products[file.product_id] = await get_product(file.product_id, session=session)
        else:
            product = products[file.product_id]

        if not product:
            return None

        if product.category_id not in categories:
            category = categories[product.category_id] = await get_category(product.category_id, session=session)
        else:
            category = categories[product.category_id]

        if not category:
            return None

        product.quantity -= 1
        category.total_products -= 1

    await session.commit()
    return product_files


@optional_session
async def get_transaction_product_files(transaction_id: int | str, /, session: AsyncSession) -> list[ProductFile] | None:
    transaction_id, = str2int(transaction_id)
    query = select(ProductFile).where(ProductFile.transaction_id == transaction_id)
    result = await session.scalars(query)
    return result.all()
