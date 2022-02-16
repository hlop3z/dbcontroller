"""
    * Database Specific (Decode)
"""

from bson.objectid import ObjectId

from .ids import ID


def sql_id_decode(unique_id):
    try:
        return_value = int(ID.decode(unique_id))
    except Exception:
        return_value = None
    return return_value


def mongo_id_decode(unique_id):
    try:
        return_value = ObjectId(ID.decode(unique_id))
    except Exception:
        return_value = None
    return return_value