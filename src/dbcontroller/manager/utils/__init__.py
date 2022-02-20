"""[summary]
Mongo & SQL - Object-Manager (Utils)
"""

from .object_id import mongo_id_decode, sql_id_decode
from .pagination import pagination
from .response import Response
from .row_handler import to_obj


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
