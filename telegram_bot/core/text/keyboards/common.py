from dataclasses import dataclass
from aiogram.utils.i18n import lazy_gettext as _


@dataclass(slots=True)
class MainMenu:
    placeholder = _('Select action')

    buy = _('Buy')
    support = _('Support')
    english = _('English')
    russian = _('Russian')

    @classmethod
    def replies(cls):
        """ Return main menu text items """
        return cls.buy, cls.support, cls.english, cls.russian
