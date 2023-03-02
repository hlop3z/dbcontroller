"""Test - Library
"""

import asyncio
import os
import pathlib
import sys

import pytest


def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)

# Test
import dbcontroller as dbc

# Config
mongo = dbc.Controller(mongo="mongodb://localhost:27017/test_database")

# Types
@mongo.model(table_name="main_user")
class UserMongo:
    name: str
    notes: dbc.text
    meta: dbc.json
    disabled: bool = False


# Init Objects
dbc.load([UserMongo])


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


class ID:
    @classmethod
    async def one(cls):
        results = await UserMongo.objects.all()
        return results.data[0].id


@pytest.mark.asyncio
async def test_create():
    results = await UserMongo.objects.create({"name": "jane doll"})
    assert results.error == False and results.data.name == "jane doll"


@pytest.mark.asyncio
async def test_update():
    selector = await ID.one()
    form = {
        "name": "joe doe",
    }
    results = await UserMongo.objects.update(selector, form)
    assert results.error == False and results.data.name == "joe doe"


@pytest.mark.asyncio
async def test_detail():
    selector = await ID.one()
    results = await UserMongo.objects.detail(selector)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_get_by():
    results = await UserMongo.objects.get_by(name="joe doe")
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_find_one():
    query = {"name": {"$regex": "joe"}}
    results = await UserMongo.objects.find_one(query)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_delete():
    selector = await ID.one()
    results = await UserMongo.objects.delete(selector)
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_all():
    await UserMongo.objects.create([{"name": "joe doe"}, {"name": "jane doll"}])
    results = await UserMongo.objects.all()
    assert (
        results.error == False
        and isinstance(results.data, list) == True
        and len(results.data) == 2
    )


@pytest.mark.asyncio
async def test_filter_by():
    query = {"name": "joe doe"}
    results = await UserMongo.objects.filter_by(
        search=query, page=1, limit=100, sort_by="-id"
    )
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_find():
    search = [{"name": {"$regex": "joe"}}, {"name": {"$regex": "jane"}}]
    query = {"$or": search}
    results = await UserMongo.objects.find(query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_search():
    search_value = "j"
    columns = ["name", "notes"]
    results = await UserMongo.objects.search(
        columns=columns, value=search_value, page=1, limit=100, sort_by="-id"
    )
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_query_list():
    query = UserMongo.objects.query_list(
        [["name", "contains", "jane"], "or", ["name", "contains", "joe"]]
    )
    results = await UserMongo.objects.find(query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_reset():
    results = await UserMongo.objects.delete(None, all=True)
    assert results.error == False


@pytest.mark.asyncio
async def demo_example():
    selector = await ID.one()
    form = {
        "name": "joe doe",
    }
    # results = await UserMongo.objects.update(selector, form)
    results = await UserMongo.objects.update(selector, form)
    print(results)


# asyncio.run(demo_example())
