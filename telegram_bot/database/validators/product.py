from core.text import escape_md_v2
from database.utils import str2float


# TODO raise ValueError instead of return None and show detailed message to user

def validate_product_name(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError("Product name must be a string.")

    name = escape_md_v2(name.strip())
    return name


def validate_product_description(name: str) -> str:
    if not isinstance(name, str):
        raise ValueError("Product description must be a string.")

    name = escape_md_v2(name.strip())
    return name


def validate_product_price(price: str) -> float:
    try:
        price, = str2float(price)
        return price
    except ValueError:
        pass
