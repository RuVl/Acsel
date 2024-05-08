class PlisioException(Exception):
    """
    Plisio Exception.
    """


class PlisioAPIException(PlisioException):
    """ Plisio API exception """

    def __init__(self, json_res: dict):
        self.status = json_res.get('status')
        data = json_res.get('data')

        if data is not None:
            self.name = data.get('name')
            self.code = data.get('code')
            self.message = data.get('message')

    def __str__(self) -> str:
        return f'PlisioAPIError(status={self.status}, name={self.name}, code={self.code}): {self.message}'


class PlisioResponseException(PlisioException):
    """ Plisio Request Exception """

    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f'PlisioResponseException: {self.message}'
