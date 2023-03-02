"""
    * Mongo-Querying
"""
import re
from typing import Any


def mongo_regex(data, ignore=False):
    """Mongo Regex Builder"""
    config = [data]
    if ignore:
        config.append(re.IGNORECASE)
    return re.compile(*config)


def where_base(key: str, operation: str, val: Any):
    """Standard Querying For Tables"""

    extra = ""
    if operation.startswith("!"):
        operation = operation[1:]
        extra = "!"

    match operation:
        case "eq":
            return_value = [[key, extra + "eq", val]]
        case "ne":
            return_value = [[key, extra + "ne", val]]
        case "lt":
            return_value = [[key, extra + "lt", val]]
        case "le":
            return_value = [[key, extra + "lte", val]]
        case "gt":
            return_value = [[key, extra + "gt", val]]
        case "ge":
            return_value = [[key, extra + "gte", val]]
        case "contains":
            return_value = [[key, extra + "regex", mongo_regex(val, True)]]
        case "regex":
            return_value = [[key, extra + "regex", mongo_regex(val)]]
        case "iregex":
            return_value = [[key, extra + "regex", mongo_regex(val, True)]]
        case "in":
            return_value = [[key, extra + "in", val]]
        case "bt":
            return_value = [
                [key, extra + "gte", val[0]],
                "and",
                [key, extra + "lte", val[1]],
            ]
    return return_value


def query_builder(data):
    """Mongo Query Builder"""
    query = {}
    operator = None
    subqueries = []

    for item in data:
        if isinstance(item, list):
            column = item[0]
            op = item[1]
            value = item[2]
            if op.startswith("!"):
                op = op[1:]
                expression = {"$not": {"$" + op: value}}
            else:
                expression = {"$" + op: value}
            subquery = {column: expression}
            subqueries.append(subquery)
        elif item == "and":
            operator = "and"
        elif item == "or":
            operator = "or"
            if len(subqueries) == 1:
                subquery = subqueries.pop()
            else:
                subquery = {"$and": subqueries}
                subqueries = []
            query = (
                {"$or": [query, subquery]} if operator == "or" and query else subquery
            )
        else:
            raise ValueError("Invalid operator")

    if subqueries:
        subquery = {"$and": subqueries} if len(subqueries) > 1 else subqueries[0]
        query = {"$or": [query, subquery]} if operator == "or" and query else subquery

    return query


class BinaryExpression:
    """Mongo SQL-Where-Style"""

    def __init__(self, *value):
        self._query = []
        self.value = where_base(*value)
        self._query.extend(self.value)

    @property
    def query(self):
        """Transform List to Query"""
        return query_builder(self._query)

    def __or__(self, obj):
        """Bitwise OR"""
        if isinstance(obj, BinaryExpression):
            self._query.append("or")
            self._query.extend(obj.value)
            return self
        raise ValueError("Must be an instance of BinaryExpression class")

    def __and__(self, obj):
        """Bitwise AND"""
        if isinstance(obj, BinaryExpression):
            self._query.append("and")
            self._query.extend(obj.value)
            return self
        raise ValueError("Must be an instance of BinaryExpression class")
