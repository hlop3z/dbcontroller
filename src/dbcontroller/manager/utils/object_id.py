"""
    * Database Specific (Decode)
"""

try:
    from bson.objectid import ObjectId
except ImportError:
    ObjectId = None

from .ids import ID


def sql_id_decode(unique_id) -> int | None:
    """Decoder for SQL"""
    try:
        return_value = int(ID.decode(unique_id))
    except Exception:
        return_value = None
    return return_value


def mongo_id_decode(unique_id) -> str | None:
    """Decoder for Mongo"""
    try:
        return_value = ObjectId(ID.decode(unique_id))
    except Exception:
        return_value = None
    return return_value


class Decode:
    """Convert ID to <SQL or Mongo> ID's Type."""

    @staticmethod
    def mongo(graphql_id):
        """ID Decode to Mongo"""
        return mongo_id_decode(graphql_id)

    @staticmethod
    def sql(graphql_id):
        """ID Decode to SQL"""
        return sql_id_decode(graphql_id)
