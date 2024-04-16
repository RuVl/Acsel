import re

from babel.support import LazyProxy


def escape_md_v2(text: str | None) -> str | None:
    """ Escape str or return None if None is provided """

    if text is None:
        return None

    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


class MarkdownMessages(type):
    def __getattribute__(cls, attr):
        value = object.__getattribute__(cls, attr)

        if attr.startswith('__') or not isinstance(value, (LazyProxy, str)):
            return value

        return escape_md_v2(value)
