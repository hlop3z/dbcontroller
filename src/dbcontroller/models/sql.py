""" SQLAlchemy Manager

Column:
    * primary_key
    * nullable
    * index
    * unique
"""
import functools
import typing
from collections import OrderedDict, namedtuple

from .. import manager
from ..core.custom_class import Globals

try:
    import sqlalchemy
    from sqlalchemy.orm import declarative_base

    SQLALCHEMY_ACTIVE = True
    SA = sqlalchemy
except ImportError:
    SQLALCHEMY_ACTIVE = False
    SA = None
    declarative_base = None

try:
    from databases import Database
except ImportError:
    Database = None

DatabaseManager = namedtuple("SQL", ["base", "database", "controller"])

# CORE Fields
ALL_FIELDS = [
    "String",
    "Text",
    "Integer",
    "Float",
    "Boolean",
    "Date",
    "DateTime",
    "Time",
    "Decimal",
    "ID",
    "TEXT",
    "JSON",
]

# Init Fields
Scalar = {key: key for key in ALL_FIELDS}

# Map SQL
if SQLALCHEMY_ACTIVE:
    # Column = SA.Column(SA.Integer, primary_key=True)
    # Fields
    Scalar["String"] = SA.String(length=255)
    Scalar["Integer"] = SA.Integer
    Scalar["Float"] = SA.Float
    Scalar["Boolean"] = SA.Boolean
    Scalar["Date"] = SA.Date
    Scalar["DateTime"] = SA.DateTime
    Scalar["Time"] = SA.Time
    Scalar["Decimal"] = SA.String(length=255)
    # Custom
    Scalar["ID"] = SA.Integer
    Scalar["Text"] = SA.Text
    Scalar["JSON"] = SA.JSON


def column_base_setup(name: str, config: dict) -> dict:
    """Column Base"""
    return {
        "primary_key": name in config.get("primary_key", []),
        "index": name in config.get("index", []),
        "unique": name in config.get("unique", []),
        "nullable": not name in config.get("required", []),
    }


def column_setup(*fields, name: str = None, config: dict = None) -> SA.Column:
    """Column Setup"""
    setup = column_base_setup(name, config)
    return SA.Column(*fields, **setup)


def sql_fields(annotations, config) -> OrderedDict:
    """All Column(s) Setup"""
    db_fields = OrderedDict()
    related_fields = OrderedDict()
    for field in annotations:
        column = functools.partial(column_setup, name=field.name, config=config)
        if field.is_custom_type:
            my_class = Globals.get(field.real)
            class_config = my_class.__spoc__.config
            related = class_config["table_name"]
            match class_config["engine"]:
                case "sql":
                    sql_scalar = column(SA.Integer, SA.ForeignKey(f"{related}._id"))
                case _:
                    sql_scalar = column(SA.String(length=255))
            if field.name not in config["ignore"]:
                related_fields[f"{field.name}_id"] = sql_scalar
        else:
            if field.name not in config["ignore"]:
                db_fields[field.name] = column(Scalar.get(field.scalar))
    for key, val in related_fields.items():
        db_fields[key] = val
    return db_fields


def sql_orm(
    base: typing.Any = None,
    original_object: typing.Any = None,
    setup: typing.Any = None,
):
    """SQLAlchemy ORM Setup"""
    return type(f"SQL{original_object.__name__}", (base,), setup).__table__


def sql_model(
    controller: typing.Any = None,
    original_object: typing.Any = None,
    annotations: typing.Any = None,
    config: dict = None,
    new_object: typing.Any = None,
):
    """Model Setup"""
    sqlalchemy_class_setup = {
        "__tablename__": config["table_name"],
        "__table_args__": [],
        "_id": SA.Column(SA.Integer, primary_key=True),
    }
    sql_cols = sql_fields(annotations, config)
    for setup in config["unique_together"]:
        unique_together = SA.UniqueConstraint(*setup)
        sqlalchemy_class_setup["__table_args__"].append(unique_together)

    sqlalchemy_class_setup["__table_args__"] = tuple(
        sqlalchemy_class_setup["__table_args__"]
    )
    for key, val in sql_cols.items():
        if key != "id":
            sqlalchemy_class_setup[key] = val
    objects = sql_orm(
        controller.base, original_object=original_object, setup=sqlalchemy_class_setup
    )
    # Finally
    new_object.__database__ = "sql"
    new_object.objects = controller.controller(objects)
    return new_object


def create_sql_manager(url: str):
    """Create SQL Base-Manager"""
    base = declarative_base()
    database = Database(url)
    controller = functools.partial(manager.SQL, database=database)
    return DatabaseManager(base=base, database=database, controller=controller)
