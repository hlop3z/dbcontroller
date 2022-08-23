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

import motor.motor_asyncio

# Test
import dbcontroller as dbc

# Config
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"

# Engine
ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


# Base
Base = ENGINE[DATABASE_NAME]

# Model
model = dbc.Model(mongo=Base)

# Types
@model.mongo(table_name="main_user")
class User:
    name: str
    notes: dbc.Text
    meta: dbc.JSON
    disabled: bool = False


# Database Admin
table = dbc.Mongo(User)


# Core: ['collection', 'crud', 'table']
# Querying: ['all', 'create', 'delete', 'detail', 'filter_by', 'find', 'find_one', 'get_by', 'id_decode', 'search', 'update']
# Querying: ['all', 'create', 'delete', 'detail', 'filter_by', 'find', 'find_one', 'get_by', 'id_decode', 'search', 'update']
# User-Input: ['form', 'form_update']
dbc.Admin.register([User])  # ... <All Other Models>
dbc.Admin.load()
dbc.Admin.types


class ID:
    @classmethod
    async def one(cls):
        results = await table.all()
        return results.data[0].id


@pytest.mark.asyncio
async def test_create():
    results = await table.create({"name": "jane doll"})
    assert results.error == False and results.data.name == "jane doll"


@pytest.mark.asyncio
async def test_update():
    selector = await ID.one()
    form = {
        "name": "joe doe",
    }
    results = await table.update(selector, form)
    assert results.error == False and results.data.name == "joe doe"


@pytest.mark.asyncio
async def test_detail():
    selector = await ID.one()
    results = await table.detail(selector)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_get_by():
    results = await table.get_by(name="joe doe")
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_find_one():
    query = {"name": {"$regex": "joe"}}
    results = await table.find_one(query)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_delete():
    selector = await ID.one()
    results = await table.delete(selector)
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_all():
    await table.create({"name": "joe doe"})
    await table.create({"name": "jane doll"})
    results = await table.all()
    assert (
        results.error == False
        and isinstance(results.data, list) == True
        and len(results.data) == 2
    )


@pytest.mark.asyncio
async def test_filter_by():
    query = {"name": "joe doe"}
    results = await table.filter_by(search=query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_find():
    search = [{"name": {"$regex": "joe"}}, {"name": {"$regex": "jane"}}]
    query = {"$or": search}
    results = await table.find(query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_search():
    search_value = "j"
    columns = ["name", "notes"]
    results = await table.search(
        columns=columns, value=search_value, page=1, limit=100, sort_by="-id"
    )
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_reset():
    results = await table.delete(None, all=True)
    assert results.error == False


@pytest.mark.asyncio
async def demo_example():
    selector = await ID.one()
    form = {
        "name": "joe doe",
    }
    results = await table.update(selector, form)
    print(results)


asyncio.run(demo_example())
