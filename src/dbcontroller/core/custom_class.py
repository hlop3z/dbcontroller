"""
    Custom Class Creator
"""
import dataclasses as dc
import typing
from collections import OrderedDict

from .scalars import SCALAR_FIELD, STRAWBERRY_CORE


class Globals:
    """API Globals"""

    @staticmethod
    def set(key, value):
        """Set"""
        globals().update({key: value})

    @staticmethod
    def get(key):
        """Get"""
        return globals().get(key)


class BaseClass:
    """API Base Class"""

    _id: typing.Optional[str] = None
    id: typing.Optional[SCALAR_FIELD.ID] = None


def create_class(custom_class, original_object, model):
    """Create Class for API"""
    ordered_annotations = OrderedDict()
    unordered_annotations = {
        **BaseClass.__annotations__,
    }
    dataclass = dc.dataclass(original_object)
    fields = dc.fields(dataclass)
    for field in fields:
        if field.name not in model.methods:
            f_default = isinstance(field.default, dc._MISSING_TYPE)
            f_default_factory = isinstance(field.default_factory, dc._MISSING_TYPE)
            out_default = dc.field(default=None)
            out_type = model.annotations[field.name].graphql
            if not f_default and f_default_factory:
                out_default = dc.field(default=field.default)
            elif f_default and not f_default_factory:
                out_default = dc.field(default_factory=field.default_factory)
            setattr(custom_class, field.name, out_default)
            unordered_annotations[field.name] = out_type

    # Set Method Fields
    for field in model.methods:
        current_method = getattr(original_object, field)
        if STRAWBERRY_CORE:
            current_method = STRAWBERRY_CORE.field(current_method)
            setattr(custom_class, field, current_method)

    # Create Annotations
    for field in ["_id", "id"] + model.fields:
        anno = unordered_annotations[field]
        ordered_annotations[field] = anno

    custom_class.__annotations__ = {**ordered_annotations}
    return custom_class


def create_custom_type(original_object, model):
    """Create Custom Class"""
    class_name = original_object.__name__
    custom_class = type(
        class_name,
        (BaseClass,),
        {},
    )
    custom_class = create_class(custom_class, original_object, model)

    # Strawberry
    if STRAWBERRY_CORE:
        custom_class = STRAWBERRY_CORE.type(custom_class, description=original_object.__doc__)
    elif not STRAWBERRY_CORE:
        custom_class = dc.dataclass(custom_class)

    # Register Global
    Globals.set(class_name, custom_class)

    return custom_class
