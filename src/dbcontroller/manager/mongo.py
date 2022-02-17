"""[summary]
Mongo Manager
"""

import functools

from .utils import Response, mongo_id_decode, pagination, to_obj


class MongoBase:
    """[summary]
    Mongo Manager (CORE)
    """

    def __init__(self, database=None, client=None):
        self.database = client[database]

    async def create(self, table: str, obj: dict) -> Response:
        """CREATE"""
        collection = self.database[table]
        try:
            if "id" in obj:
                del obj["id"]
            result = await collection.insert_one(obj)
            instance = await collection.find_one({"_id": {"$eq": result.inserted_id}})
            result = Response(data=to_obj(instance))
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    async def update(self, table: str, search: dict, form: dict) -> Response:
        """UPDATE"""
        collection = self.database[table]
        try:
            instance = await collection.update_many(search, {"$set": form})
            count = instance.modified_count
            result = Response(count=count)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    async def delete(self, table: str, search: dict) -> Response:
        """DELETE"""
        collection = self.database[table]
        try:
            instance = await collection.delete_many(search)
            count = instance.deleted_count
            result = Response(count=count)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    async def find_one(self, table: str, search: dict) -> Response:
        """DETAIL"""
        collection = self.database[table]
        count = 0
        try:
            instance = await collection.find_one(search)
            if instance:
                count = 1
            result = Response(data=to_obj(instance), count=count)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result

    async def find(
        self, table: str, search: dict, page: int = 1, limit: int = 100
    ) -> Response:
        """FIND"""
        collection = self.database[table]
        try:
            _page = pagination(page=page, limit=limit)
            cursor = collection.find(search)
            cursor.skip(_page.offset).limit(_page.limit)
            items = [i async for i in cursor]
            count = await collection.count_documents(search)
            result = Response(data=to_obj(items), count=count)
        except Exception as error:
            result = Response(error=True, message=str(error))
        return result


class MongoCrud:
    """[summary]
    Mongo Manager (CRUD)
    """

    def __init__(self, table=None, database=None, client=None):
        self.mongo = MongoBase(database=database, client=client)
        self.table = table

    @staticmethod
    def id_decode(unique_id):
        """ID-DECODER"""
        return mongo_id_decode(unique_id)

    """
    ..####...#####...######...####...######..######.
    .##..##..##..##..##......##..##....##....##.....
    .##......#####...####....######....##....####...
    .##..##..##..##..##......##..##....##....##.....
    ..####...##..##..######..##..##....##....######.
    """

    async def create(self, form: dict):
        """CREATE"""
        return await self.mongo.create(self.table, form)

    """
    .##..##..#####...#####....####...######..######.
    .##..##..##..##..##..##..##..##....##....##.....
    .##..##..#####...##..##..######....##....####...
    .##..##..##......##..##..##..##....##....##.....
    ..####...##......#####...##..##....##....######.
    """

    async def update(self, form: dict):
        """UPDATE"""
        ids = form.get("id")
        if not isinstance(ids, list):
            ids = [ids]
        _id = [mongo_id_decode(i) for i in ids]
        search = {"_id": {"$in": _id}}
        del form["id"]
        results = await self.mongo.update(self.table, search, form)
        if results.count == 1 and not results.error:
            return await self.detail(ids[0])
        return results

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
        _id = [mongo_id_decode(i) for i in ids]
        search = {"_id": {"$in": _id}}
        return await self.mongo.delete(self.table, search)

    """
    .#####...######...####...#####............####...##..##..######.
    .##..##..##......##..##..##..##..........##..##..###.##..##.....
    .#####...####....######..##..##..######..##..##..##.###..####...
    .##..##..##......##..##..##..##..........##..##..##..##..##.....
    .##..##..######..##..##..#####............####...##..##..######.
    """

    async def detail(self, unique_id: str):
        """DETAIL"""
        _id = mongo_id_decode(unique_id)
        search = {"_id": {"$eq": _id}}
        results = await self.mongo.find_one(self.table, search)
        if results.count == 1:
            results.data = results.data
        return results

    async def find_one(self, search: dict = {}):
        """FIND-ONE"""
        return await self.mongo.find_one(self.table, search)

    """
    .#####...######...####...#####...........##......######...####...######.
    .##..##..##......##..##..##..##..........##........##....##........##...
    .#####...####....######..##..##..######..##........##.....####.....##...
    .##..##..##......##..##..##..##..........##........##........##....##...
    .##..##..######..##..##..#####...........######..######...####.....##...
    """

    async def find(self, search: dict = {}, page: int = 1, limit: int = 100):
        """FIND"""
        return await self.mongo.find(self.table, search=search, page=page, limit=limit)


def mongo_client(database, client):
    """MongoCrud-Wrapper"""
    return functools.partial(MongoCrud, database=database, client=client)


def mongo(client):
    """MongoClient-Wrapper"""
    return functools.partial(mongo_client, client=client)
