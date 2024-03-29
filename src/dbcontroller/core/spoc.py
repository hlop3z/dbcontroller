"""
    Components
"""

import dataclasses as dc
import functools
import typing

COMPONENT = {}

COMPONENT["model"] = {"engine": "dbcontroller", "type": "model"}
COMPONENT["form"] = {"engine": "dbcontroller", "type": "form"}


@dc.dataclass(frozen=True)
class Component:
    """Spoc Plugin"""

    config: typing.Any = None
    metadata: typing.Any = None
    is_spoc_plugin: bool = True


def component(
    cls: object = None,
    *,
    config: dict = None,
    metadata: dict = None,
) -> typing.Any:
    """Plugin Creator"""

    config = config or {}
    metadata = metadata or {}
    if cls is None:
        return functools.partial(
            component,
            config=config,
            metadata=metadata,
        )

    # Real Wrapper
    cls.__spoc__ = Component(config=config, metadata=metadata)
    return cls


def is_model(cls):
    """Plugin Validator"""
    return cls.__spoc__.metadata == COMPONENT["model"]


def is_form(cls):
    """Plugin Validator"""
    return cls.__spoc__.metadata == COMPONENT["form"]
