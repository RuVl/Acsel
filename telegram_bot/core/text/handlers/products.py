from dataclasses import dataclass

from aiogram.utils.i18n import lazy_gettext as _

from core.text.utils import MarkdownMessages


@dataclass(slots=True)
class CommonMessages(metaclass=MarkdownMessages):
    greeting = _('Welcome to our auto-sale service.\n'
                 'Be sure to read the "Rules and FAQ" before using the service!')
    support = _('For any questions, please contact @TEST')

    choose_category = _('Choose product category')


@dataclass(slots=True)
class PrivilegeMessages(metaclass=MarkdownMessages):
    ask_category_name = _('Send name of category')
