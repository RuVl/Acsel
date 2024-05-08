from database.utils import escape_md_v2, str2float, str2int


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


def validate_product_price(price: str | float) -> float:
    try:
        price, = str2float(price)
        return price
    except ValueError:
        pass


def validate_product_quantity(quantity: str | int, max_quantity: int = None) -> int:
    try:
        quantity, = str2int(quantity)
    except ValueError:
        return

    if quantity < 0:
        return

    if max_quantity is not None and quantity > max_quantity:
        return

    return quantity
