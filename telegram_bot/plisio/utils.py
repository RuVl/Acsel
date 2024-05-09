import logging

from aiohttp import ContentTypeError, ClientResponse

from plisio.exceptions import PlisioAPIException, PlisioResponseException

logger = logging.getLogger('plisio')


# noinspection PyUnusedLocal
async def log_get_requests(session, method, url, params):
    logger.info(f"GET request to {url} with params: {params}")


async def validate_response(response: ClientResponse) -> dict:
    try:
        data: dict = await response.json()
    except ContentTypeError as e:
        raise PlisioResponseException('Invalid JSON response from plisio') from e

    if not 200 <= response.status < 300 or data.get('status') != 'success':
        raise PlisioAPIException(data)

    return data
