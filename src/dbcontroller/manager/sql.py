"""
    * SQLAlchemy + Databases — Controller
"""

import functools
import math
from types import SimpleNamespace

from .utils import (
    Decode,
    Objects,
    Response,
    clean_form,
    clean_update_form,
    fixed_id_column,
)
from .utils.sql_where import Filters as SQLFilters

try:
    from sqlalchemy.sql.elements import BinaryExpression
except ImportError:
    BinaryExpression = None

try:
    from databases import Database
except ImportError:

    def Database(x):
        """Fake Database"""
        return SimpleNamespace(database_url=x)


class SQL:
    """SQlAlchemy & Databases (Manager)

    -----------------------------------------------------------------------------------------------
    # Init
    -----------------------------------------------------------------------------------------------
    sql = SQLBase(database_url, custom_type)

    -----------------------------------------------------------------------------------------------
    # Form
    -----------------------------------------------------------------------------------------------
    - Clean-Inputs      : sql.form(dict)
    - Clean-Empty       : sql.form_update(dict)

    -----------------------------------------------------------------------------------------------
    # Read (Examples)
    -----------------------------------------------------------------------------------------------
    - Get-By(Single-Row): await sql.get_by(id=1, name="spongebob")
    - Custom-Find-One   : await sql.find_one(sql.Q.where("id", "eq", 1))
    - Filter-By         : await sql.filter_by(id=1, name="spongebob", page=1, etc...)
    - Search-Columns    : await sql.search(["name", "title"], "bob", page=1, etc...)
    - Custom-Querying   : await sql.find(
                                    sql.Q.where("id", "in", [1, 2, 3]),
                                    page=1, limit=100, sort_by='-id'
                                )

    -----------------------------------------------------------------------------------------------
    # C.U.D
    -----------------------------------------------------------------------------------------------
    - Create            : await sql.create(dict)
    - Update            : await sql.update(items: list[IDs], values: dict)
    - Delete            : await sql.delete(items: list[IDs])
    """

    def __init__(self, database_url, custom_type):
        """Start Manager"""
        self.database = Database(database_url)
        self.table = custom_type.objects
        self.Q = SQLFilters(custom_type.objects)
        self.where = self.Q.where
        self.form = functools.partial(
            clean_form, custom_type, custom_type.objects.columns.keys()
        )
        self.form_update = functools.partial(
            clean_update_form, custom_type, custom_type.objects.columns.keys()
        )
        self.columns = self.table.columns.keys()
        self.c = self.table.c

    @staticmethod
    def id_decode(unique_id):
        """ID-DECODER"""
        return Decode.sql(unique_id)

    async def create(self, form: dict | list) -> Response:
        """CREATE/CREATE-MANY"""
        if isinstance(form, dict):
            return await self.create_one(form)
        return await self.create_many(form)

    async def create_one(self, form: dict):
        """Create Single-Row."""
        # Init Values
        return_value = Response()
        unique_id = False
        try:
            sql_query = self.table.insert(form)
            unique_id = await self.database.execute(sql_query)
            if unique_id:
                # If Success => Fetch Row
                return_value.data = await self.get_by(_id=unique_id)
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        return return_value

    async def create_many(self, form: list):
        """Create Multiple-Row."""
        # Init Values
        return_value = Response()
        try:
            sql_query = self.table.insert()
            unique_ids = await self.database.execute_many(sql_query, values=form)
            return_value.data = unique_ids
            return_value.count = len(form)
        except Exception as error:
            print("*" * 24)
            print(error)
            print("*" * 24)
            return_value.error = True
            return_value.error_message = str(error)
        return return_value

    async def update(self, unique_ids: list[str], form: dict):
        """Update Multiple/Single-Row(s)"""
        return_value = Response()
        # Get Ids
        if not isinstance(unique_ids, list):
            unique_ids = [unique_ids]
        all_ids = [Decode.sql(i) for i in unique_ids]
        sql_ids_in = self.Q.where("_id", "in", all_ids)
        try:
            return_value.count = await self.database.execute(
                self.table.update().where(sql_ids_in).values(**form)
            )
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        # Get Details
        if len(all_ids) == 1 and return_value.count == 1:
            return_value.data = await self.get_by(_id=all_ids[0])
        return return_value

    async def delete(self, unique_ids: list[str], all: bool = False):
        """Delete Multiple/Single-Row(s)"""
        return_value = Response()
        # Get Ids
        if not isinstance(unique_ids, list):
            unique_ids = [unique_ids]
        if not all:
            all_ids = [Decode.sql(i) for i in unique_ids]
            sql_ids_in = self.Q.where("_id", "in", all_ids)
            selector = self.table.delete().where(sql_ids_in)
        else:
            selector = self.table.delete()
        try:
            return_value.count = await self.database.execute(selector)
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        return return_value

    async def detail(self, ID):
        """Get Single-Row from Database Table by ID"""
        query = self.Q.filter_by(_id=Decode.sql(ID))
        item = await self.database.fetch_one(self.Q.select(query))
        return Objects.sql(item)

    async def get_by(self, **kwargs):
        """Get Single-Row from Database Table by <Keyword-Arguments>"""
        kwargs = fixed_id_column(kwargs)
        query = self.Q.filter_by(**kwargs)
        item = await self.database.fetch_one(self.Q.select(query))
        return Objects.sql(item)

    async def find_one(self, query):
        """Get Single-Row from Database Table by <SQLAlchemy-BinaryExpression>"""
        item = await self.database.fetch_one(self.Q.select(query))
        return Objects.sql(item)

    async def all(
        self,
    ):
        """Get All-Rows from Database Table"""
        items = await self.database.fetch_all(self.Q.select())
        return Response(data=Objects.sql(items), count=len(items), pages=1)

    async def find(
        self,
        search: BinaryExpression = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <SQLAlchemy-BinaryExpression>"""
        sort_by = fixed_id_column(sort_by)
        try:
            query = self.Q.find(search, page=page, limit=limit, sort_by=sort_by)
            items = await self.database.fetch_all(query.query)
            count = await self.database.fetch_val(query.count)
            _limit = limit or 1
            pages = int(math.ceil(count / _limit))
            return Response(data=Objects.sql(items), count=count, pages=pages)
        except Exception as e:
            print(e)
            return Response(data=[], count=0, pages=0)

    async def filter_by(
        self,
        search: dict | None = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <Keyword-Arguments>"""
        search = fixed_id_column(search)
        query = self.Q.filter_by(**search) if search else None
        items = await self.find(query, page=page, limit=limit, sort_by=sort_by)
        return items

    async def search(
        self,
        columns: list | None = None,
        value: str | None = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str | None = None,
    ):
        """Get Multiple-Rows from Database Table by <Searching-Columns>"""
        query = self.Q.search(columns, value) if value else None
        items = await self.find(query, page=page, limit=limit, sort_by=sort_by)
        return items
