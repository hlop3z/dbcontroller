"""
    Databases Manager (SQL & MongoDB)
"""
import functools
from collections import namedtuple

from .. import manager
from ..manager.sql import Database as SQLDatabase
from .model import Model

try:
    import motor.motor_asyncio

    MotorClient = motor.motor_asyncio.AsyncIOMotorClient
except ImportError:
    MotorClient = False

try:
    from sqlalchemy.orm import declarative_base

except ImportError:
    declarative_base = False


DBManager = namedtuple("DBManager", ["base", "client", "database"])
DBController = namedtuple("DBController", ["sql", "mongo", "keys"])
Controller = namedtuple("Controller", ["sql", "mongo"])
MongoDNS = namedtuple("MongoDNS", ["url", "database"])


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


def databases_setup(sql: str = None, mongo: str = None):
    """Databases Setup"""
    # SQL
    sql_manager = DBManager(base=None, client=None, database=None)
    if declarative_base and sql:
        sql_base = declarative_base()
        sql_client = functools.partial(manager.SQL, sql)
        sql_manager = DBManager(
            base=sql_base, client=sql_client, database=SQLDatabase(sql)
        )

    # Mongo
    mongo_manager = DBManager(base=None, client=None, database=None)
    if MotorClient and mongo:
        mongo_dns = get_database_info(mongo)
        mongo_core = MotorClient(mongo_dns.url)
        # To Be Used
        mongo_base = mongo_core[mongo_dns.database]
        mongo_client = manager.Mongo
        mongo_manager = DBManager(
            base=mongo_base, client=mongo_client, database=mongo_base
        )

    return Controller(sql=sql_manager, mongo=mongo_manager)


class Database:
    """Database Models"""

    def __init__(self, sql: str = None, mongo: str = None, fastberry: bool = False):
        # Init
        self.fastberry = fastberry
        self._core_models = {}
        self._managers = {}
        self._model = Model()
        self._manager_sql = None
        self._manager_mongo = None
        self._base = None
        # Config Databases
        self._config(sql=sql, mongo=mongo)

    def _config(self, sql: str = None, mongo: str = None):
        """Config Databases"""
        # Core
        type_base = Model()
        app_managers = {
            "sql": type_base.type,
            "mongo": type_base.type,
        }
        the_manager = databases_setup(sql=sql, mongo=mongo)
        self._manager_sql = the_manager.sql
        self._manager_mongo = the_manager.mongo
        self._base = the_manager.sql.base
        if declarative_base:
            active = Model(sql=the_manager.sql.base)
            app_managers["sql"] = active.sql
        if MotorClient:
            active = Model(mongo=the_manager.mongo.base)
            app_managers["mongo"] = active.mongo
        # self._model = Model(sql=the_manager.sql.base, mongo=the_manager.mongo.base)
        self._model = Controller(**app_managers)

    def register(self, all_models: list):
        """Register a Type(Model)"""
        if not isinstance(all_models, list):
            all_models = [all_models]
        for current_type in all_models:
            self._core_models[current_type.__meta__.table_uri] = current_type

    def load(self):
        """Load Lazy-Tables"""
        for current_type in self._core_models.values():
            if current_type._lazy_object:
                if callable(current_type.objects):
                    current_type.objects()

    def set_fastberry(self, mode: bool = True):
        """Set Fastberry"""
        self.fastberry = mode

    @property
    def base(self):
        """SQLAlchemy Base"""
        return self._base

    @property
    def db(self):
        """Databases SQL & Mongo"""
        return self.database

    @property
    def database(self):
        """Databases SQL & Mongo"""
        return Controller(
            sql=self._manager_sql.database,
            mongo=self._manager_mongo.database,
        )

    @property
    def types(self):
        """Types"""
        return self._core_models

    @property
    def model(self):
        """Base SQL & Mongo"""
        return self._model

    @property
    def manager_sql(self):
        """Manager SQL"""
        return self._manager_sql

    @property
    def manager_mongo(self):
        """Manager Mongo"""
        return self._manager_mongo

    @property
    def manager(self):
        """Manager Mongo"""
        return self._managers

    def manage(self, all_models: list):
        """Register + Load"""
        if not self.fastberry:
            self.register(all_models)
            self.load()
        # Dicts
        manager_sql = {}
        manager_mongo = {}
        for current_type in all_models:
            if hasattr(current_type, "__meta__"):
                name = current_type.__meta__.table_uri
                is_sql = current_type.__meta__.sql
                is_mongo = current_type.__meta__.mongo
                if is_sql and declarative_base:
                    manager_sql[name] = self.manager_sql.client(current_type)
                elif is_mongo and MotorClient:
                    manager_mongo[name] = self.manager_mongo.client(current_type)

        all_keys = list(manager_sql.keys()) + list(manager_mongo.keys())
        db_manager = DBController(
            sql=manager_sql, mongo=manager_mongo, keys=lambda: all_keys
        )
        self._managers = db_manager
        return db_manager
