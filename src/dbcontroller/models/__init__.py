"""
    (Manager) - SQL & Mongo
"""
import functools
import typing

from .mongo import create_mongo_manager, mongo_model
from .sql import create_sql_manager, sql_model


def create_model(
    new_object: typing.Any = None,
    engine: str = None,
    original_object: typing.Any = None,
    annotations: typing.Any = None,
    config: typing.Any = None,
    base: typing.Any = None,
):
    """Create { SQL } or { Mongo }"""
    db_model = None
    match engine:
        case "sql":
            db_model = functools.partial(
                sql_model,
                controller=base,
                original_object=original_object,
                annotations=annotations,
                config=config,
                new_object=new_object,
            )
        case "mongo":
            db_model = functools.partial(
                mongo_model,
                controller=base,
                table_name=config["table_name"],
                annotations=annotations,
                config=config,
                new_object=new_object,
            )
    return db_model


def create_database(
    sql: typing.Any = None,
    mongo: typing.Any = None,
):
    """Create Database"""
    if sql:
        return create_sql_manager(sql)
    return create_mongo_manager(mongo)
