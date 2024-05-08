import hashlib
import hmac
import json
import logging

from fastapi import APIRouter, Response, HTTPException, Depends, Body

from api.env import PlisioKeys
from api.models.plisio import StatusRequest
from database import session_maker
from database.enums import TransactionStatuses
from database.methods.transaction import get_transaction_by_txn_id

router = APIRouter(
    prefix='/plisio',
    tags=['plisio']
)

logger = logging.getLogger('plisio')


def validate_hash(data: StatusRequest = Body(...)):
    logger.info(f'Validate transaction ({data.txn_id}) hash')

    ordered_data = data.model_dump()
    ordered_data.pop('verify_hash')
    string_to_sign = json.dumps(ordered_data)
    calculated_hash = hmac.new(PlisioKeys.API_TOKEN.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).hexdigest()

    if calculated_hash == data.verify_hash:
        return data

    logger.info(f'Hashes are not equals. Calculated: {calculated_hash}, received: {data.verify_hash}, string_to_sign: {string_to_sign}')
    raise HTTPException(status_code=422, detail='Hash verification failed')


@router.post('/status')
async def status(data: StatusRequest = Depends(validate_hash)):
    logger.info(f'Update transaction ({data.txn_id}) status to {data.status}')

    async with session_maker() as session:
        transaction = await get_transaction_by_txn_id(data.txn_id, session=session)
        if transaction is None:
            logger.warning(f'Transaction with txn_id {data.txn_id} not found')
            raise HTTPException(status_code=404, detail='Transaction not found')

        transaction.status = TransactionStatuses(data.status)
        transaction.confirmations = data.confirmations

        transaction.amount = data.amount
        transaction.currency = data.currency

        transaction.source_amount = data.source_amount
        transaction.source_currency = data.source_currency
        transaction.source_status = data.source_status

        transaction.comment = data.comment

        transaction.invoice_commission = data.invoice_commission
        transaction.invoice_sum = data.invoice_sum
        transaction.invoice_total_sum = data.invoice_total_sum

        await session.commit()

    return Response(status_code=200)
