from pathlib import Path
from shutil import copy2

from sqlalchemy.ext.asyncio import AsyncSession

from core.env import MainKeys
from database.models import ProductFile
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
