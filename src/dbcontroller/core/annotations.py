"""
    Annotations
"""

import dataclasses as dc
import typing
from collections import OrderedDict

from .scalars import JSON, TEXT, Scalar

CUSTOM_SCALARS = [TEXT, JSON]


@dc.dataclass(frozen=True)
class AnnotationInfo:
    """Annotation Setup"""

    name: str
    scalar: str
    graphql: typing.Any
    original: typing.Any
    real: typing.Any
    optional: bool = False
    is_list: bool = False
    is_json: bool = False
    is_custom_type: bool = False


@dc.dataclass(frozen=True)
class Model:
    """Annotation Setup"""

    fields: typing.Any
    methods: typing.Any
    annotations: typing.Any


def make_annotation(
    real: typing.Any = None,
    is_list: bool = False,
    is_custom_type: bool = False,
):
    """Make Annotations"""

    col_type = real

    if is_custom_type:
        col_type = typing.ForwardRef(col_type)
    if is_list:
        col_type = typing.List[col_type]

    col_type = typing.Optional[col_type]

    return col_type


def get_field_annotation_core(single_annotation: typing.Any, found_args: tuple):
    """Field Core Annotation"""
    core_arg = None
    has_children = []

    # Core Arg
    if found_args:
        core_arg = found_args[0]
    else:
        core_arg = single_annotation

    # Core Arg Continued . . .
    has_children = typing.get_args(core_arg)
    if len(has_children) > 0:
        core_arg = has_children[0]
        if isinstance(core_arg, str):
            core_arg = typing.ForwardRef(core_arg)
    return core_arg


def get_annotations_args(field_name: str, single_annotation: typing.Any):
    """Get: Custom Annotations"""
    found_args = typing.get_args(single_annotation)
    real_arg = get_field_annotation_core(single_annotation, found_args)
    is_custom_type = isinstance(real_arg, typing.ForwardRef)
    is_optional = type(None) in found_args
    is_list = False
    is_dict = False
    scalar_name = None

    if isinstance(real_arg, str):
        is_custom_type = True

    if isinstance(real_arg, typing.ForwardRef):
        real_arg = real_arg.__forward_arg__

    scalar_field = Scalar.get(real_arg)
    if real_arg in CUSTOM_SCALARS:
        real_arg = scalar_field.python

    # IS -> List <YES or NO>
    if found_args and len(typing.get_args(found_args[0])) > 0:
        is_list = True

    # IS -> Step 1 ...
    if len(found_args) == 1:
        is_list = True

    # IS -> Step 2 ...
    if real_arg == JSON:
        is_dict = True

    # IS -> Step 3 ...
    if scalar_field:
        scalar_name = scalar_field.name

    # IS -> Step 4 ...
    graphql = make_annotation(
        real_arg,
        is_list=is_list,
        is_custom_type=is_custom_type,
    )

    # Custom Annotations
    return AnnotationInfo(
        name=field_name,
        scalar=scalar_name,
        original=single_annotation,
        real=real_arg,
        optional=is_optional,
        is_list=is_list,
        is_json=is_dict,
        is_custom_type=is_custom_type,
        graphql=graphql,
    )


def get_args(original_object):
    """Get Annotations"""
    real_annotations = original_object.__annotations__
    field_keys = list(real_annotations.keys())
    func_annotations = [
        x for x in dir(original_object) if not x.startswith("_") and x not in field_keys
    ]
    cool_annotations = OrderedDict()
    for key, val in real_annotations.items():
        found_args = get_annotations_args(key, val)
        cool_annotations[key] = found_args
    for key in func_annotations:
        func = getattr(original_object, key)
        val = func.__annotations__.get("return")
        found_args = get_annotations_args(key, val)
        cool_annotations[key] = found_args
    return Model(
        fields=field_keys, methods=func_annotations, annotations=cool_annotations
    )


# is_list
# is_json
# optional
# is_custom_type
