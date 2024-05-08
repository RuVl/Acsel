import re
from typing import Iterator


def escape_md_v2(text: str | None) -> str | None:
    """ Escape str for telegram (MarkdownV2) """
    if isinstance(text, str):
        return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


def str2int(*args) -> Iterator[int]:
    for value in args:
        yield int(value) if isinstance(value, str) else value


def str2float(*args) -> Iterator[float]:
    for value in args:
        yield float(value) if isinstance(value, str) else value
