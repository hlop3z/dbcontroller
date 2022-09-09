"""
    Mongo Manager
"""
import functools
import typing
from collections import OrderedDict, namedtuple

from .. import manager
from ..core.custom_class import Globals

try:
    import motor.motor_asyncio

    SQLALCHEMY_ACTIVE = True
    PM = motor.motor_asyncio
except ImportError:
    SQLALCHEMY_ACTIVE = False
    PM = None


MongoDNS = namedtuple("MongoDNS", ["url", "database"])
DatabaseManager = namedtuple("Mongo", ["base", "database", "controller"])


def mongo_fields(annotations, config) -> OrderedDict:
    """All Column(s) Setup"""
    db_fields = OrderedDict({"_id": True})
    related_fields = OrderedDict()
    for field in annotations:
        if field.is_custom_type:
            if field.name not in config["ignore"]:
                related_fields[f"{field.name}_id"] = True
        else:
            if field.name not in config["ignore"]:
                db_fields[field.name] = True

    for key in related_fields.keys():
        db_fields[key] = True
    return db_fields


def mongo_model(
    controller: typing.Any = None,
    table_name: str = None,
    annotations: typing.Any = None,
    config: dict = None,
    new_object: typing.Any = None,
):
    """Mongo ORM Setup"""
    fields = mongo_fields(annotations, config)
    objects = controller.base[table_name]
    # Finally
    db_keys = list(fields.keys())
    new_object.__database__ = "mongo"
    new_object.objects = controller.controller(objects, keys=db_keys)
    return new_object


def get_database_name(url):
    """Get Table's Name from URL"""
    items = url.split("/")[-1::]
    return items[0] if len(items) == 1 else None


def get_database_url(url):
    """Get Database's URL"""
    return "/".join(url.split("/")[:-1])


def get_database_info(url):
    """{ get_database_name } + { get_database_url }"""
    return MongoDNS(url=get_database_url(url), database=get_database_name(url))


def create_mongo_manager(url: str):
    """Create Mongo Base-Manager"""
    info = get_database_info(url)
    engine = PM.AsyncIOMotorClient(info.url)
    database = engine[info.database]
    controller = functools.partial(manager.Mongo, database=database)
    return DatabaseManager(base=database, database=database, controller=controller)
