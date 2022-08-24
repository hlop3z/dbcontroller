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
from sqlalchemy.orm import declarative_base

import dbcontroller as dbc

# URL
DATABASE_URL = "sqlite:///data/example.db"

# Base
Base = declarative_base()

# Setup
engine = create_engine(DATABASE_URL, echo=True)

model = dbc.Model(sql=Base)
SQL = functools.partial(dbc.SQL, DATABASE_URL)

# Types
@model.sql(table_name="main_user")
class UserSQL:
    name: str
    notes: dbc.Text
    meta: dbc.JSON
    disabled: bool = False


table = SQL(UserSQL)


class ID:
    one = "MTo6YTU1ZTUzMmVhYjAyOGI0Mg=="
    two = "Mjo6M2VmOWFiYmI1ZGY1YjY0MQ=="


def test_create_database():
    Base.metadata.create_all(engine)
    assert True


@pytest.mark.asyncio
async def test_create():
    results = await table.create({"name": "jane doll"})
    assert results.error == False and results.data.name == "jane doll"


@pytest.mark.asyncio
async def test_update():
    selector = ID.one
    form = {
        "name": "joe doe",
    }
    results = await table.update(selector, form)
    assert results.error == False and results.data.name == "joe doe"


@pytest.mark.asyncio
async def test_detail():
    selector = ID.one
    results = await table.detail(selector)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_get_by():
    results = await table.get_by(id=1)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_find_one():
    query = table.where("name", "contains", "joe")
    results = await table.find_one(query)
    assert results.name == "joe doe"


@pytest.mark.asyncio
async def test_delete():
    selector = ID.one
    results = await table.delete(selector)
    assert results.error == False and results.count == 1


@pytest.mark.asyncio
async def test_all():
    await table.create([{"name": "joe doe"}, {"name": "jane doll"}])
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
    query = table.where("name", "contains", "jane") | table.where(
        "name", "contains", "joe"
    )
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


async def demo_example():
    query = table.where("name", "contains", "joe")
    results = await table.find_one(query)
    assert results.name == "joe doe"


# asyncio.run(demo_example())
