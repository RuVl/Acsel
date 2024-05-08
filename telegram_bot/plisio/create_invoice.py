import aiohttp

from plisio.env import PlisioKeys
from plisio.utils import validate_response


async def create_invoice(
        order_name: str,
        order_number: str | int,
        currency: str = None,
        amount: float | str = None,
        source_currency: str = None,
        source_amount: float | str = None,
        allowed_psys_cids=None,
        description: str = None,
        callback_url: str = None,
        success_callback_url: str = None,
        fail_callback_url: str = None,
        email: str = None,
        language='en_US',
        redirect_to_invoice=None,
        expire_min: int | str = None) -> dict:
    """ https://plisio.net/documentation/endpoints/create-an-invoice """

    data = {
        'order_name': order_name,
        'order_number': str(order_number),
        'currency': currency,
        'amount': str(amount),
        'source_currency': source_currency,
        'source_amount': str(source_amount),
        'allowed_psys_cids': allowed_psys_cids,
        'description': description,
        'callback_url': callback_url,
        'success_callback_url ': success_callback_url,
        'fail_callback_url': fail_callback_url,
        'email': email,
        'language': language,
        'redirect_to_invoice': redirect_to_invoice,
        'api_key': PlisioKeys.API_TOKEN,
        'expire_min': str(expire_min)
    }

    async with aiohttp.ClientSession() as session:
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

        async with session.get('https://plisio.net/api/v1/invoices/new', params=data) as resp:
            return validate_response(resp)
