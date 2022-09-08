"""
    Database Controller
"""
import dataclasses as dc
import functools
import typing

from .dbmanager import Database


@dc.dataclass(frozen=True)
class DatabaseController:
    """Single Controller"""

    name: str
    engine: str
    model: typing.Any
    admin: typing.Any
    database: typing.Any
    base: typing.Any = None


@dc.dataclass(frozen=True)
class Controller:
    """Full Controller"""

    sql: typing.Any
    mongo: typing.Any


def create_database_manager(
    all_models: list, engine_type: str = None, active_db: typing.Any = None
):
    """Create a { Database Manager }"""
    if not isinstance(all_models, list):
        all_models = [all_models]
    match engine_type:
        case "sql":
            manager = active_db.manage(all_models).sql  # .database .base
        case "mongo":
            manager = active_db.manage(all_models).mongo
    return manager


def create_database(name: str, engine_type: str, url: str, fastberry: bool = False):
    """Create a { Database }"""
    active_database = None
    custom_database = None
    match engine_type:
        case "sql":
            active_database = Database(sql=url, fastberry=fastberry)
            active_admin = functools.partial(
                create_database_manager,
                engine_type=engine_type,
                active_db=active_database,
            )
            custom_database = DatabaseController(
                name=name,
                engine=engine_type,
                admin=active_admin,
                model=active_database.model.sql,
                database=active_database.database.sql,
                base=active_database.base,
            )
        case "mongo":
            active_database = Database(mongo=url, fastberry=fastberry)
            active_admin = functools.partial(
                create_database_manager,
                engine_type=engine_type,
                active_db=active_database,
            )
            custom_database = DatabaseController(
                name=name,
                engine=engine_type,
                admin=active_admin,
                model=active_database.model.mongo,
                database=active_database.database.mongo,
            )
    return custom_database


def process_databases(
    databases: dict, engine_type: str = "sql", fastberry: bool = False
):
    """Process all { Databases }"""
    active_db = databases.get(engine_type)
    all_dbs = {}
    if active_db:
        for db_name, db_url in active_db.items():
            manager = create_database(db_name, engine_type, db_url, fastberry)
            all_dbs[db_name] = manager
    return all_dbs


def create_controllers(databases, fastberry: bool = False):
    """Controller Builder"""
    mongo_dbs = process_databases(databases, "mongo", fastberry=fastberry)
    sql_dbs = process_databases(databases, "sql", fastberry=fastberry)
    return Controller(sql=sql_dbs, mongo=mongo_dbs)
