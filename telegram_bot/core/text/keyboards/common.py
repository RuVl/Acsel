from dataclasses import dataclass

from aiogram.utils.i18n import lazy_gettext as _

from core.text.utils import InstanceMessages


@dataclass(slots=True)
class MainMenuCKbMessages(InstanceMessages):
    placeholder = _('Select action')

    buy = _('Buy')
    support = _('Support')

    add_category = _('Add category')
    add_product = _('Add product')
    add_product_files = _('Add files')

    english = _('English')
    russian = _('Russian')

    @classmethod
    def all_replies(cls):
        return cls.privilege_replies() + cls.common_replies()

    @classmethod
    def common_replies(cls):
        return cls.buy, cls.support, cls.english, cls.russian

    @classmethod
    def privilege_replies(cls):
        return cls.add_category, cls.add_product, cls.add_product_files
