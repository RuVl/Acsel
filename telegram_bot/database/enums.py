import enum


@enum.verify(enum.NAMED_FLAGS)
class UserRights(enum.IntFlag, boundary=enum.STRICT):
    """ Telegram core user's rights """

    CAN_WRITE = 0b001  # Blocked or not
    CAN_BUY = 0b010  # Can buy products
    CAN_PARTICIPATE_AUCTION = 0b100  # Can take part in an auction sale

    CAN_ADD_FILE = 0b001 << 3  # Can add new products in stock
    CAN_ADD_PRODUCT = 0b010 << 3  # Can add new products in stock
    CAN_ADD_CATEGORY = 0b100 << 3  # Can add new categories of products

    BANNED = 0
    USER = CAN_WRITE | CAN_BUY | CAN_PARTICIPATE_AUCTION
    MODERATOR = USER | CAN_ADD_PRODUCT | CAN_ADD_FILE
    ADMIN = MODERATOR | CAN_ADD_CATEGORY
