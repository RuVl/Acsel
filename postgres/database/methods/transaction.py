from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Transaction
from database.methods.product_file import reserve_product_files
from database.methods.utils import optional_session
from database.utils import str2int


@optional_session
async def create_transaction(transaction: Transaction, /, session: AsyncSession) -> Transaction | None:
    session.add(transaction)

    files = await reserve_product_files(transaction.files, session=session)
    if not files:
        return None

    await session.commit()
    await session.refresh(transaction)

    return transaction


@optional_session
async def get_transaction(transaction_id: int | str, session: AsyncSession) -> Transaction | None:
    transaction_id, = str2int(transaction_id)
    query = select(Transaction).where(Transaction.id == transaction_id)
    return await session.scalar(query)


@optional_session
async def get_transaction_by_txn_id(txn_id: str, /, session: AsyncSession) -> Transaction | None:
    query = select(Transaction).where(Transaction.txn_id == txn_id)
    return await session.scalar(query)
