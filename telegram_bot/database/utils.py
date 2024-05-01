from typing import Iterator


def str2int(*args) -> Iterator[int]:
    for value in args:
        yield int(value) if isinstance(value, str) else value


def str2float(*args) -> Iterator[float]:
    for value in args:
        yield float(value) if isinstance(value, str) else value
