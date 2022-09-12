"""
    Base
"""

import functools

from ..models import create_model
from .annotations import get_args
from .custom_class import create_custom_type
from .spoc import COMPONENT, component
from .table import table_info

# from .tools import get_module_name, to_pascal_case


def custom_type(
    original_object: object = None,
    *,
    table_name: str = None,
    primary_key: list = None,
    required: list = None,
    index: list = None,
    unique: list = None,
    unique_together: list = None,
    ignore: list = None,
    engine: str = "sql",
    database: str = "default",
    controller: object = None,
    description:str = None,
):
    """{ Controller } for GraphQL { Type } & { Model } Database"""
    primary_key = primary_key or []
    required = required or []
    index = index or []
    unique = unique or []
    unique_together = unique_together or []
    ignore = ignore or []

    config = {
        "table_name": table_name,
        "primary_key": primary_key,
        "required": required,
        "index": index,
        "unique": unique,
        "unique_together": unique_together,
        "ignore": ignore,
        "engine": engine,
        "database": database,
        "controller": controller,
    }

    # Starting Wrapper. . .
    if original_object is None:
        return functools.partial(
            custom_type,
            **config,
            description=description,
        )

    # Annotations (Python)
    model = get_args(original_object)

    # GraphQL (Strawberry) Class
    custom_class = create_custom_type(original_object, model, description)
    table_config = table_info(original_object, table_name, config)
    db_table_name = table_config.table_name
    config["table_name"] = db_table_name

    # Databases - (DBController)
    custom_class.__database__ = None
    if controller is not None:
        db_model = create_model(
            base=controller,
            new_object=custom_class,
            engine=engine,
            original_object=original_object,
            annotations=model.annotations.values(),
            config=config,
        )
        custom_class.__database__ = db_model

    # Component - (Spoc)
    component_config = {
        "table_name": db_table_name,
        "database": database,
        "engine": engine,
        "annotations": model.annotations,
    }
    component(custom_class, config=component_config, metadata=COMPONENT["model"])

    # Return: Customized Class
    return custom_class
