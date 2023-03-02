"""
    * SQLAlchemy + Databases — Controller
"""
# import functools
import math
from functools import partial

from .utils import Objects  # clean_form, clean_update_form,
from .utils import Decode, Response, fixed_id_column
from .utils.sql_where import Filters as SQLFilters

try:
    from sqlalchemy.sql.elements import BinaryExpression
except ImportError:
    BinaryExpression = None


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

    def __init__(self, objects=None, database=None):
        """Start Manager"""
        self.database = database
        self.table = objects
        self.Q = SQLFilters(objects)
        self.where = self.Q.where
        self.columns = self.table.columns.keys()
        self.c = self.table.c
        self.to_obj = partial(Objects.sql, self.columns)

    @staticmethod
    def id_decode(unique_id):
        """ID-DECODER"""
        return Decode.sql(unique_id)

    async def create(
        self, form: dict | list = None, return_items: bool = True
    ) -> Response:
        """CREATE/CREATE-MANY"""
        if isinstance(form, dict):
            return await self.create_one(form)
        return await self.create_many(form, return_items)

    async def _create_one_row(self, form: dict) -> Response:
        """(Base) Create Single-Row."""
        return_value = Response()
        try:
            sql_query = self.table.insert().values(**form)
            return_value.data = await self.database.execute(sql_query)
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        return return_value

    async def create_one(self, form: dict):
        """Create Single-Row."""
        return_value = await self._create_one_row(form)
        if return_value.data and not return_value.error:
            return_value.data = await self.get_by(_id=return_value.data)
        return return_value

    async def _create_many_rows(self, form: list):
        """(Base) Create Multiple-Row."""
        return_value = Response()
        try:
            sql_query = self.table.insert()
            unique_ids = await self.database.execute_many(sql_query, values=form)
            return_value.data = unique_ids
            return_value.count = len(form)
        except Exception as error:
            return_value.error = True
            return_value.error_message = str(error)
        return return_value

    async def create_many(self, forms: list, return_items: bool):
        """Create Single-Row."""
        if return_items:
            all_ids = []
            for form in forms:
                return_value = await self._create_one_row(form)
                if return_value.data:
                    all_ids.append(return_value.data)
            sql_ids_in = self.Q.where("_id", "in", all_ids)
            items = await self.database.fetch_all(self.Q.select(sql_ids_in))
            return Response(data=self.to_obj(items), count=len(items))
        return await self._create_many_rows(forms)

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
        return self.to_obj(item)

    async def get_by(self, **kwargs):
        """Get Single-Row from Database Table by <Keyword-Arguments>"""
        kwargs = fixed_id_column(kwargs)
        query = self.Q.filter_by(**kwargs)
        item = await self.database.fetch_one(self.Q.select(query))
        return self.to_obj(item)

    async def find_one(self, query):
        """Get Single-Row from Database Table by <SQLAlchemy-BinaryExpression>"""
        item = await self.database.fetch_one(self.Q.select(query))
        return self.to_obj(item)

    async def all(
        self,
    ):
        """Get All-Rows from Database Table"""
        items = await self.database.fetch_all(self.Q.select())
        return Response(data=self.to_obj(items), count=len(items), pages=1)

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
            return Response(data=self.to_obj(items), count=count, pages=pages)
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

    def query_list(self, data: list | None = None):
        """Array of SQL.where(s)"""
        query = None
        operator = None

        for item in data:
            if isinstance(item, list):
                column = item[0]
                op = item[1]
                value = item[2]
                expression = self.where(column, op, value)
                if query is None:
                    query = expression
                else:
                    if operator == "and":
                        query = query & expression
                    elif operator == "or":
                        query = query | expression
            elif item == "and":
                operator = "and"
            elif item == "or":
                operator = "or"
        return query
