from dataclasses import dataclass

from aiogram.utils.i18n import lazy_gettext as _

from core.text.utils import MarkdownMessages, InstanceFormatMessages
from database.models import Category, Product


@dataclass(slots=True)
class CommonMessages(metaclass=MarkdownMessages):
    greeting = _('Welcome to our auto-sale service.\n'
                 'Be sure to read the "Rules and FAQ" before using the service!')
    support = _('For any questions, please contact @TEST')

    choose_category = _('Choose product category')
    choose_product = _('Choose product')


@dataclass(slots=True)
class PrivilegeMessages(metaclass=MarkdownMessages):
    # === Create category ===
    ask_category_name = _('Send name of category')
    invalid_category_name = _('Invalid category name!')

    # === Create product ===
    select_category = _('Select category')  # And for add product files

    ask_product_name = _('Send name of product')
    invalid_product_name = _('Invalid product name!')

    ask_product_description = _('Send description of product')
    invalid_product_description = _('Invalid product description!')

    ask_product_price = _('Send price of product')
    invalid_product_price = _('Invalid product price!')

    # === Add product files ===
    select_product = _('Select product')
    ask_product_files = _('Send files of product')
    download_file_error = _('File download failed 😭\n Please try again')
    success_add_product_file = _('Product file created')


@dataclass(slots=True)
class CategoryMessages(InstanceFormatMessages, metaclass=MarkdownMessages):
    def __init__(self, category: Category):
        super(CategoryMessages, self).__init__(category=category)

    create_info_ = _('Category: `{category.name}`')


@dataclass(slots=True)
class ProductMessages(InstanceFormatMessages, metaclass=MarkdownMessages):
    def __init__(self, product: Product, category: Category):
        super(ProductMessages, self).__init__(product=product, category=category)

    create_info_ = _('Product: `{product.name}`\n'
                     ' · description: `{product.description}`\n'
                     ' · price: $`{product.price}`\n'
                     ' · category: `{category.name}`')

    buy_info_ = _('You have chosen: *{category.name}* - *{product.name}*\n'
                  '{product.description}\n'
                  'Available for purchase: *{product.quantity}*\n'
                  'Price per unit: $*{product.price}*\n\n'
                  '_Enter the desired amount of product or use the buttons below_')

    sure2buy_ = _('Order details\n'
                  'Product name: {category.name} - {product.name}\n'
                  'Quantity: {product.quantity}\n'
                  'Total amount: ${product.price * product.quantity}\n')
