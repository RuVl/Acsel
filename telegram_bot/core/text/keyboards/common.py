from dataclasses import dataclass

from aiogram.utils.i18n import lazy_gettext as _


@dataclass(slots=True)
class MainMenuCKbMessages:
    placeholder = _('Select action')

    buy = _('Buy')
    support = _('Support')

    add_category = _('Add category')
    add_product = _('Add product')

    english = _('English')
    russian = _('Russian')

    @classmethod
    def all_replies(cls):
        return cls.admin_replies() + cls.user_replies()

    @classmethod
    def user_replies(cls):
        return cls.buy, cls.support, cls.english, cls.russian

    @classmethod
    def admin_replies(cls):
        return cls.add_category, cls.add_product
