"""[summary]
Mongo & SQL - Object-Manager (Utils)
"""

from .object_id import mongo_id_decode, sql_id_decode
from .pagination import pagination
from .response import Response
from .row_handler import to_obj
from .sql_forms import clean_form, clean_update_form


class Objects:
    """Convert <SQL or Mongo> output to types.SimpleNamespace => Object(s)."""

    @staticmethod
    def mongo(items):
        """Convert Mongo to SimpleNamespace"""
        return to_obj(items)

    @staticmethod
    def sql(items):
        """Convert SQLAlchemy to SimpleNamespace"""
        return to_obj(items, sql=True)


class ReadID:
    """Convert ID to <SQL or Mongo> ID's Type."""

    @staticmethod
    def mongo(ID):
        """ID Decode to Mongo"""
        return mongo_id_decode(ID)

    @staticmethod
    def sql(ID):
        """ID Decode to SQL"""
        return sql_id_decode(ID)
