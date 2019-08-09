import re

from toolz import compose
from unidecode import unidecode


def to_snake_case(string: str) -> str:
    fns = [
        lambda x: re.sub('(.)([A-Z][a-z]+)', r'\1_\2', x),
        lambda x: re.sub('([a-z0-9])([A-Z])', r'\1_\2', x),
        lambda x: x.lower(),
        lambda x: x.split("_"),
        lambda x: filter(lambda s: s != "", x),
        lambda x: "_".join(x)
    ]

    return compose(*reversed(fns))(string)


def to_normalized_string(original_name: str) -> str:
    ascii_name = to_lowercase_ascii(original_name)
    return re.sub(r'[^\w]+', '_', ascii_name)


def to_lowercase_ascii(unicode_string: str) -> str:
    return to_ascii(unicode_string).lower()


def to_ascii(unicode_string: str) -> str:
    return unidecode(unicode_string)
