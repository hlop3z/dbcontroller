"""[summary]
SQL Manager
"""

import functools

import sqlalchemy as sa
from sqlalchemy import func, select

from .utils import Response, pagination, sql_id_decode, to_obj


class ManagerCrud:
    """[summary]
    SQL Manager (CORE)
    """

    def __init__(self, model=None, database=None) -> None:
        self.database = database
        self.table = model.__table__

    """
    ..####...#####...######...####...######..######.
    .##..##..##..##..##......##..##....##....##.....
    .##......#####...####....######....##....####...
    .##..##..##..##..##......##..##....##....##.....
    ..####...##..##..######..##..##....##....######.
    """

    async def create(self, obj: dict) -> Response:
        """CREATE"""
        try:
            # Setup
            create = self.table.insert()
            if "id" in obj:
                del obj["id"]
            sql_query = create.values(**obj)
            # Run
            unique_id = await self.database.execute(sql_query)
            # Detail
            find = self.table.select()
            sql_query = find.filter_by(id=unique_id)
            instance = await self.database.fetch_one(sql_query)
            result = Response(data=to_obj(instance, sql=True))
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    """
    .##..##..#####...#####....####...######..######.
    .##..##..##..##..##..##..##..##....##....##.....
    .##..##..#####...##..##..######....##....####...
    .##..##..##......##..##..##..##....##....##.....
    ..####...##......#####...##..##....##....######.
    """

    async def update(self, form: dict):
        """UPDATE"""
        try:
            # Setup
            ids = form.get("id")
            if not isinstance(ids, list):
                ids = [ids]
            _id = [sql_id_decode(i) for i in ids]
            update = self.table.update()
            sql_ids_in = self.table.c.id.in_(_id)
            find_ids = self.table.select().where(sql_ids_in)
            del form["id"]
            sql_query = update.where(sql_ids_in).values(**form)
            # Run
            updates = await self.database.execute(sql_query)
            if updates == 1:
                # Detail
                instance = await self.database.fetch_one(find_ids)
                result = Response(data=to_obj(instance, sql=True), count=updates)
            else:
                result = Response(count=updates)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    """
    .#####...######..##......######..######..######.
    .##..##..##......##......##........##....##.....
    .##..##..####....##......####......##....####...
    .##..##..##......##......##........##....##.....
    .#####...######..######..######....##....######.
    """

    async def delete(self, ids: list):
        """DELETE"""
        if not isinstance(ids, list):
            ids = [ids]
        _id = [sql_id_decode(i) for i in ids]
        delete = self.table.delete()
        sql_ids_in = self.table.c.id.in_(_id)
        sql_query = delete.where(sql_ids_in)
        try:
            deleted = await self.database.execute(sql_query)
            result = Response(count=deleted)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    """
    .#####...######...####...#####............####...##..##..######.
    .##..##..##......##..##..##..##..........##..##..###.##..##.....
    .#####...####....######..##..##..######..##..##..##.###..####...
    .##..##..##......##..##..##..##..........##..##..##..##..##.....
    .##..##..######..##..##..#####............####...##..##..######.
    """

    async def detail(self, unique_id: str) -> Response:
        """DETAIL"""
        _id = sql_id_decode(unique_id)
        # Detail
        find = self.table.select()
        sql_query = find.filter_by(id=_id)
        try:
            instance = await self.database.fetch_one(sql_query)
            result = Response(data=to_obj(instance, sql=True))
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    """
    .#####...######...####...#####...........##......######...####...######.
    .##..##..##......##..##..##..##..........##........##....##........##...
    .#####...####....######..##..##..######..##........##.....####.....##...
    .##..##..##......##..##..##..##..........##........##........##....##...
    .##..##..######..##..##..#####...........######..######...####.....##...
    """

    async def find(
        self,
        query: str = None,
        page: int = 1,
        limit: int = 100,
    ):
        """FIND"""
        _page = pagination(page=page, limit=limit)
        sql_query = self.table.select().where(query)
        sql_query = sql_query.offset(_page.offset).limit(_page.limit)
        get_count = select([func.count()]).where(query)
        try:
            items = await self.database.fetch_all(sql_query)
            count = await self.database.fetch_all(get_count.select_from(self.table))
            result = Response(data=to_obj(items, sql=True), count=count[0][0])
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    """
    ..####...##..##..######..#####...##..##..######..##..##...####..
    .##..##..##..##..##......##..##...####.....##....###.##..##.....
    .##.###..##..##..####....#####.....##......##....##.###..##.###.
    .##..##..##..##..##......##..##....##......##....##..##..##..##.
    ..#####...####...######..##..##....##....######..##..##...####..
    """

    def where(self, key, operation, val):
        """WHERE Per-Column Operator"""
        return_value = None
        col = None
        found = False
        is_not = False
        if operation.startswith("!"):
            operation = operation[1:]
            is_not = True
        if hasattr(self.table.c, key):
            col = getattr(self.table.c, key)
            found = True
        # Operator
        if found:
            match operation:
                case "eq":
                    sql_ope = getattr(col, "__eq__")
                    return_value = sql_ope(val)
                case "ne":
                    sql_ope = getattr(col, "__ne__")
                    return_value = sql_ope(val)
                case "lt":
                    sql_ope = getattr(col, "__lt__")
                    return_value = sql_ope(val)
                case "le":
                    sql_ope = getattr(col, "__le__")
                    return_value = sql_ope(val)
                case "gt":
                    sql_ope = getattr(col, "__gt__")
                    return_value = sql_ope(val)
                case "ge":
                    sql_ope = getattr(col, "__ge__")
                    return_value = sql_ope(val)
                case "contains":
                    sql_ope = getattr(col, "contains")
                    return_value = sql_ope(val)
                case "like":
                    sql_ope = getattr(col, "like")
                    return_value = sql_ope(val)
                case "ilike":
                    sql_ope = getattr(col, "ilike")
                    return_value = sql_ope(val)
                case "in":
                    sql_ope = getattr(col, "in_")
                    return_value = sql_ope(val)
                case "bt":
                    sql_ope = getattr(col, "between")
                    return_value = sql_ope(*val)
        if is_not:
            return_value = sa.not_(return_value)
        return return_value


def sql(database):
    """ManagerCrud-Wrapper"""
    return functools.partial(ManagerCrud, database=database)