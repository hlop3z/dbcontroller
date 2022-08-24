"""[summary]
Mongo & SQL - Object-Manager (Utils)
"""

from .object_id import Decode
from .pagination import pagination
from .response import Response
from .row_handler import Objects
from .sql_forms import clean_form, clean_update_form


def fixed_id_column(kwargs: dict | list | str):
    """Fixed the ID Column"""
    if isinstance(kwargs, dict):
        if kwargs.get("id"):
            kwargs["_id"] = kwargs["id"]
            del kwargs["id"]
    elif isinstance(kwargs, list):
        if "id" in kwargs:
            kwargs.remove("id")
            kwargs.append("_id")
    elif isinstance(kwargs, str):
        if kwargs == "id":
            kwargs = "_id"
        elif kwargs == "-id":
            kwargs = "-_id"
    return kwargs
