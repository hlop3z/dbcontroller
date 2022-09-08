"""
    Tool to Transform { Text } to { Code-Cases }
    Tool to Get Module's Name
"""
import re
import typing


def to_kebab_case(text):
    """Clean Text"""
    text = re.sub("[^0-9a-zA-Z]+", "-", str(text))
    return text.lower()


def to_camel_case(text):
    """Converts to { camelCase }"""
    text = to_kebab_case(text)
    init, *temp = text.title().split("-")
    return "".join([init.lower()] + temp)


def to_pascal_case(text):
    """Converts to { PascalCase }"""
    text = to_kebab_case(text)
    return text.title().replace("-", "")


def get_module_name(model: typing.Any):
    """Get: Class-Module's Name"""
    name = model.__module__
    parts = name.split(".")
    if parts[0] == "apps" and len(parts) > 1:
        parts.pop(0)
    module_name = parts[0]
    if module_name == "__main__":
        module_name = None
    return module_name
