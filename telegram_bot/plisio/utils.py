
from aiohttp import ContentTypeError, ClientResponse

from plisio.exceptions import PlisioAPIException, PlisioResponseException


async def validate_response(response: ClientResponse) -> dict:
    try:
        data: dict = response.json()
    except ContentTypeError as e:
        raise PlisioResponseException('Invalid JSON response from plisio') from e

    if not 200 <= response.status < 300 or data.get('status') != 'success':
        raise PlisioAPIException(data)

    return data
