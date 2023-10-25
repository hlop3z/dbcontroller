"""
    Mongo Manager
"""

# import functools
import math

from .utils import Objects  # clean_form, clean_update_form,
from .utils import Decode, Response, fixed_id_column, pagination
from .utils.mongo_where import BinaryExpression as MongoWhere


class MongoCrud:
    """
    Mongo Manager (CORE)
    """

    def __init__(self, client=None):
        self.collection = client

    async def create(self, form: dict | list) -> Response:
        """CREATE/CREATE-MANY"""
        if isinstance(form, dict):
            return await self.create_one(form)
        return await self.create_many(form)

    async def create_one(self, form: dict) -> Response:
        """CREATE"""
        collection = self.collection
        try:
            result = await collection.insert_one(form)
            instance = await collection.find_one({"_id": {"$eq": result.inserted_id}})
            result = Response(data=Objects.mongo(instance))
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def create_many(self, forms: list) -> Response:
        """CREATE-MANY"""
        collection = self.collection
        try:
            result = await collection.insert_many(forms)
            search = {"_id": {"$in": result.inserted_ids}}
            cursor = collection.find(search)
            items = [i async for i in cursor]
            result = Response(data=Objects.mongo(items), count=len(items))
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def update(self, search: dict = None, form: dict = None) -> Response:
        """UPDATE"""
        collection = self.collection
        try:
            instance = await collection.update_many(search, {"$set": form})
            count = instance.modified_count
            result = Response(count=count)
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def delete(self, search: dict) -> Response:
        """DELETE"""
        collection = self.collection
        try:
            instance = await collection.delete_many(search)
            count = instance.deleted_count
            result = Response(count=count)
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def find_one(self, search: dict) -> Response:
        """DETAIL"""
        collection = self.collection
        try:
            instance = await collection.find_one(search)
            result = Objects.mongo(instance)
        except Exception:
            result = None
        return result

    async def find(
        self,
        search: dict = None,
        page: int | None = None,
        limit: int | None = None,
        sort_by: str = "-id",
    ) -> Response:
        """FIND"""
        collection = self.collection
        sort_desc = 1
        # Check Sort By
        if sort_by.startswith("-"):
            sort_by = sort_by[1:]
            sort_desc = -1
        if sort_by == "id":
            sort_by = "_id"
        try:
            # Add Sort By
            cursor = collection.find(search).sort(sort_by, sort_desc)
            # Offset & Limit
            if page and limit:
                _page = pagination(page=page, limit=limit)
                cursor.skip(_page.offset).limit(_page.limit)
            items = [i async for i in cursor]
            count = await collection.count_documents(search)
            pages = int(math.ceil(count / limit))
            result = Response(data=Objects.mongo(items), count=count, pages=pages)
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result


    async def find_all(
        self,
        search: dict = None,
        sort_by: str = "-id",
    ) -> Response:
        """FIND-ALL"""
        collection = self.collection
        sort_desc = 1
        # Check Sort By
        if sort_by.startswith("-"):
            sort_by = sort_by[1:]
            sort_desc = -1
        if sort_by == "id":
            sort_by = "_id"
        try:
            # Add Sort By
            cursor = collection.find(search).sort(sort_by, sort_desc)
            items = [i async for i in cursor]
            result = Response(data=Objects.mongo(items), count=len(items), pages=1)
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def all(self):
        """ALL-Rows"""
        collection = self.collection
        cursor = collection.find()
        items = [i async for i in cursor]
        return Response(data=Objects.mongo(items), count=len(items), pages=1)


class Mongo:
    """
    Mongo Manager (CRUD)
    """

    def __init__(self, objects=None, database=None, keys=None):
        self.collection = database
        self.crud = MongoCrud(objects)
        self.columns = keys
        self.where = MongoWhere

    @staticmethod
    def id_decode(unique_id):
        """ID-DECODER"""
        return Decode.mongo(unique_id)

    async def create(self, form: dict):
        """Create Single-Row."""
        return await self.crud.create(form)

    async def update(self, unique_ids: list[str], form: dict):
        """Update Multiple/Single-Row(s)"""
        if not isinstance(unique_ids, list):
            unique_ids = [unique_ids]
        _ids = [Decode.mongo(i) for i in unique_ids]
        search = {"_id": {"$in": _ids}}
        results = await self.crud.update(search, form)
        if results.count == 1 and not results.error:
            results.data = await self.detail(unique_ids[0])
        return results

    async def delete(self, unique_ids: list[str], all: bool = False):
        """Delete Multiple/Single-Row(s)"""
        if not all:
            if not isinstance(unique_ids, list):
                unique_ids = [unique_ids]
            _id = [Decode.mongo(i) for i in unique_ids]
            search = {"_id": {"$in": _id}}
        else:
            search = {}
        return await self.crud.delete(search)

    async def detail(self, unique_id: str):
        """Get Single-Row from Database Collection by ID"""
        _id = Decode.mongo(unique_id)
        search = {"_id": {"$eq": _id}}
        return await self.crud.find_one(search)

    async def get_by(self, **kwargs):
        """Get Single-Row by <Keyword-Arguments>"""
        kwargs = fixed_id_column(kwargs)
        search = {key: {"$eq": val} for key, val in kwargs.items()}
        return await self.crud.find_one(search)

    async def find_one(self, search: dict = None):
        """Get Single-Row from Database Collection"""
        return await self.crud.find_one(search)

    async def all(self):
        """Get All-Rows from Database"""
        return await self.crud.all()

    async def find(
        self, search: dict = None, page: int = 1, limit: int = 100, sort_by: str = "-id"
    ):
        """Get Multiple-Rows from Database Collection"""
        sort_by = fixed_id_column(sort_by)
        return await self.crud.find(
            search=search, page=page, limit=limit, sort_by=sort_by
        )

    async def find_all(
        self, search: dict = None, sort_by: str = "-id"
    ):
        """Get Multiple-Rows from Database Collection"""
        sort_by = fixed_id_column(sort_by)
        return await self.crud.find_all(
            search=search, sort_by=sort_by
        )

    async def filter_by(
        self, search: dict = None, page: int = 1, limit: int = 100, sort_by: str = "-id"
    ):
        """Get Multiple-Rows from Database Collection by <Keyword-Arguments>"""
        search = fixed_id_column(search)
        query = {key: {"$eq": val} for key, val in search.items()}
        return await self.find(search=query, page=page, limit=limit, sort_by=sort_by)

    async def search(
        self,
        columns: list | None = None,
        value: str | None = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "-id",
    ):
        """Get Multiple-Rows from Database Collection by <Searching-Columns>"""
        search = [{key: {"$regex": value}} for key in columns]
        return await self.find({"$or": search}, page=page, limit=limit, sort_by=sort_by)

    def query_list(self, data: list | None = None):
        """Array of Mongo.where(s)"""
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
        return query.query
