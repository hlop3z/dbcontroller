"""
    Lib Utils
"""


def to_camel_case(text):
    """Converts to { camel-Case }"""
    init, *temp = text.split("_")
    return "".join([init.lower(), *map(str.title, temp)])


def to_pascal_case(text):
    """Converts to { Pascal-Case }"""
    temp = text.split("_")
    return "".join([*map(str.title, temp)])


