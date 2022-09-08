"""Test - Library
"""

import asyncio
import functools
import os
import pathlib
import sys

import pytest


def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)


import functools

# Test
from sqlalchemy import create_engine

import dbcontroller as dbc

sql = dbc.Controller(sql="sqlite:///example.db")

# Setup
engine = create_engine(sql.url, echo=True)


# Types
@sql.model(table_name="main_user")
class UserSQL:
    name: str
    notes: dbc.text
    meta: dbc.json
    disabled: bool = False

# Init Objects
dbc.load([UserSQL])
class ID:
    one = "MTo6YTU1ZTUzMmVhYjAyOGI0Mg=="
    two = "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ=="


def test_create_database():
    sql.base.metadata.create_all(engine)
    assert True


@pytest.mark.asyncio
async def test_create():
    results = await UserSQL.objects.create({"name": "jane doll"})
    assert results.error == False and results.data.name == "jane doll"


@pytest.mark.asyncio
async def test_update():
    selector = ID.one
    form = {
        "name": "joe doe",
    }
    results = await UserSQL.objects.update(selector, form)
    assert results.error == False and results.data.name == "joe doe"


@pytest.mark.asyncio
async def test_detail():
    selector = ID.one
    results = await UserSQL.objects.detail(selector)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_get_by():
    results = await UserSQL.objects.get_by(id=1)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_find_one():
    query = UserSQL.objects.where("name", "contains", "joe")
    results = await UserSQL.objects.find_one(query)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_delete():
    selector = ID.one
    results = await UserSQL.objects.delete(selector)
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_all():
    await UserSQL.objects.create([{"name": "joe doe"}, {"name": "jane doll"}])
    results = await UserSQL.objects.all()
    assert (
        results.error == False
        and isinstance(results.data, list) == True
        and len(results.data) == 2
    )


@pytest.mark.asyncio
async def test_filter_by():
    query = {"name": "joe doe"}
    results = await UserSQL.objects.filter_by(search=query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_find():
    query = UserSQL.objects.where("name", "contains", "jane") | UserSQL.objects.where(
        "name", "contains", "joe"
    )
    results = await UserSQL.objects.find(query, page=1, limit=100, sort_by="-id")
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_search():
    search_value = "j"
    columns = ["name", "notes"]
    results = await UserSQL.objects.search(
        columns=columns, value=search_value, page=1, limit=100, sort_by="-id"
    )
    assert results.error == False and results.count == 2


@pytest.mark.asyncio
async def test_reset():
    results = await UserSQL.objects.delete(None, all=True)
    assert results.error == False


async def demo_example():
    query = UserSQL.objects.where("name", "contains", "joe")
    results = await UserSQL.objects.find_one(query)
    assert results.name == "joe doe"


# asyncio.run(demo_example())
