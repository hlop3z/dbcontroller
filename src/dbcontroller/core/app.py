"""
    App
"""
import dataclasses as dc
import datetime
import decimal
import functools

from ..models import create_database
from ..tools import get_module_name
from .base import custom_type
from .spoc import is_model

DATE = datetime.date
DATETIME = datetime.datetime
TIME = datetime.time
DECIMAL = decimal.Decimal
TYPE = functools.partial(custom_type, engine=None, controller=None)


def field(method, **kwargs):
    """Default Value For Type(s)"""
    default_value = None
    if callable(method):
        default_value = dc.field(default_factory=method, **kwargs)
    else:
        default_value = dc.field(default=method, **kwargs)
    return default_value


def load(models: list):
    """Init All Models"""
    types = {}
    for active in models:
        """
        is_component = is_model(active.cls)
        if is_component:
            if hasattr(active.cls, "__database__"):
                if callable(active.cls.__database__):
                    active.cls.__database__()
                types[active.key] = active.cls
        """
        app_name = get_module_name(active)
        module_uri = f"{app_name}.{active.__name__.lower()}"
        is_component = is_model(active)
        if is_component:
            if hasattr(active, "__database__"):
                if callable(active.__database__):
                    active.__database__()
                types[module_uri] = active
    return types


class Date:
    """Datetime for Testing"""

    @staticmethod
    def date():
        """Date"""
        return datetime.date.today()

    @staticmethod
    def datetime():
        """DateTime"""
        return datetime.datetime.now()

    @staticmethod
    def time():
        """Time"""
        return datetime.datetime.now().time()


class Controller:
    """Create Full-Controller"""

    def __init__(self, sql: str = None, mongo: str = None):
        if mongo:
            engine = "mongo"
            self.url = mongo
        elif sql:
            engine = "sql"
            self.url = sql
        self.engine = engine
        self.manager = create_database(sql=sql, mongo=mongo)

    @property
    def base(self):
        """Manager"""
        return self.manager.base

    @property
    def database(self):
        """Manager"""
        return self.manager.database

    def manage(self, objects=None):
        """Manager"""
        return self.manager.controller(objects=objects)

    @property
    def model(self):
        """SQL or Mongo"""
        return functools.partial(
            custom_type, engine=self.engine, controller=self.manager
        )
