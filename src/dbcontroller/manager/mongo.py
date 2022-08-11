"""
    Mongo Manager
"""

import math

from .utils import Response, mongo_id_decode, pagination, to_obj


class MongoCrud:
    """
    Mongo Manager (CORE)
    """

    def __init__(self, client=None):
        self.collection = client

    async def create(self, form: dict) -> Response:
        """CREATE"""
        collection = self.collection
        try:
            result = await collection.insert_one(form)
            instance = await collection.find_one({"_id": {"$eq": result.inserted_id}})
            result = Response(data=to_obj(instance))
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def update(self, search: dict, form: dict) -> Response:
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
            result = to_obj(instance)
        except Exception:
            result = None
        return result

    async def find(
        self,
        search: dict,
        page: int = 1,
        limit: int = 100,
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
            _page = pagination(page=page, limit=limit)
            # Add Sort By
            cursor = collection.find(search).sort(sort_by, sort_desc)
            # Offset & Limit
            if page != -1:
                cursor.skip(_page.offset).limit(_page.limit)
            items = [i async for i in cursor]
            count = await collection.count_documents(search)
            pages = int(math.ceil(count / limit))
            result = Response(data=to_obj(items), count=count, pages=pages)
        except Exception as error:
            result = Response(error=True, error_message=str(error))
        return result

    async def all(self):
        """ALL-Rows"""
        collection = self.collection
        cursor = collection.find()
        items = [i async for i in cursor]
        return Response(data=to_obj(items), count=len(items), pages=1)


class Mongo:
    """
    Mongo Manager (CRUD)
    """

    def __init__(self, custom_type=None):
        self.collection = custom_type.objects
        self.crud = MongoCrud(custom_type.objects)

    @staticmethod
    def id_decode(unique_id):
        """ID-DECODER"""
        return mongo_id_decode(unique_id)

    async def create(self, form: dict):
        """CREATE"""
        return await self.crud.create(form)

    async def update(self, ids: list, form: dict):
        """UPDATE"""
        _ids = [mongo_id_decode(i) for i in ids]
        search = {"_id": {"$in": _ids}}
        results = await self.crud.update(search, form)
        if results.count == 1 and not results.error:
            return await self.detail(ids[0])
        return results

    async def delete(self, ids: list):
        """DELETE"""
        if not isinstance(ids, list):
            ids = [ids]
        _id = [mongo_id_decode(i) for i in ids]
        search = {"_id": {"$in": _id}}
        return await self.crud.delete(search)

    async def detail(self, unique_id: str):
        """DETAIL"""
        _id = mongo_id_decode(unique_id)
        search = {"_id": {"$eq": _id}}
        return await self.crud.find_one(search)

    async def find_one(self, search: dict = {}):
        """FIND-ONE"""
        return await self.crud.find_one(search)

    async def get_by(self, **kwargs):
        """Get Single-Row by <Keyword-Arguments>"""
        search = {key: {"$eq": val} for key, val in kwargs.items()}
        return await self.crud.find_one(search)

    async def filter_by(self, **kwargs):
        """Get Multiple-Rows from Database Table by <Keyword-Arguments>"""
        search = {key: {"$eq": val} for key, val in kwargs.items()}
        return await self.crud.find(search)

    async def search(
        self,
        columns: list | None = None,
        value: str | None = None,
        page: int = 1,
        limit: int = 100,
        sort_by: str = "-id",
    ):
        """Get Multiple-Rows from Database Table by <Searching-Columns>"""
        search = [{key: {"$regex": value}} for key in columns]
        return await self.find({"$or": search}, page=page, limit=limit, sort_by=sort_by)

    async def find(
        self, search: dict = {}, page: int = 1, limit: int = 100, sort_by: str = "-id"
    ):
        """FIND"""
        return await self.crud.find(
            search=search, page=page, limit=limit, sort_by=sort_by
        )

    async def all(self):
        """ALL-Rows"""
        return await self.crud.all()
