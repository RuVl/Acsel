from dataclasses import dataclass

from aiogram.utils.i18n import lazy_gettext as _


@dataclass(slots=True)
class UserMessages:
    greeting = _('Welcome to our auto-sale service.\n'
                 'Be sure to read the "Rules and FAQ" before using the service!')
    choose_category = _('Choose product category')
