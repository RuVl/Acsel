import re

from babel.support import LazyProxy


def escape_md_v2(text: str | None) -> str | None:
    """ Escape str for telegram (MarkdownV2) """
    if isinstance(text, str):
        return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


class LazyMessages(type):
    def __getattribute__(cls, attr: str):
        """ Convert public LazyProxy attributes to str """
        value = object.__getattribute__(cls, attr)
        if not isinstance(value, LazyProxy) or attr.startswith('_') or attr.endswith('_'):
            return value

        return str(value)


class MarkdownMessages(LazyMessages):
    def __getattribute__(cls, attr: str):
        """ Escape public str or LazyProxy attributes """
        value = super().__getattribute__(attr)
        if not isinstance(value, str) or attr.startswith('_') or attr.endswith('_'):
            return value

        return escape_md_v2(value)


class InstanceMessages:
    @staticmethod
    def _is_private_attr(attr: str) -> bool:
        return attr.startswith('__') or attr.endswith('__')

    def __getattribute__(self, attr: str):
        value = object.__getattribute__(self, attr)
        if not isinstance(value, LazyProxy) or self._is_private_attr(attr):
            return value

        return str(value)


class InstanceFormatMessages(InstanceMessages):
    def __init__(self, **kwargs):
        self.format_kwargs = kwargs

    @staticmethod
    def _should_escape(attr: str) -> bool:
        """ Should escape if attr is not ends with _ """
        return not attr.endswith('_')

    def __getattribute__(self, attr: str):
        """ Format public attributes and escape them if necessary """
        value = super().__getattribute__(attr)
        if not isinstance(value, str) or self._is_private_attr(attr):
            return value

        value = value.format(**self.format_kwargs)
        return escape_md_v2(value) if self._should_escape(attr) else value
