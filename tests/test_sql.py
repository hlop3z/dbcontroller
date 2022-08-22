"""Test - Library
"""

import asyncio
import os
import pathlib
import sys
import sqlalchemy
from types import SimpleNamespace
import functools

def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)


# Test
import dbcontroller as dbc

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DB_URL = 'sqlite:///data/authentication.db'

engine = create_engine(DB_URL, echo = True)

# Base
Base = declarative_base()

# Model
Model = dbc.Model(sql=Base)

# Types
@Model.sql
class Notes:
    text: dbc.Text
    completed: bool = False
    


# Database Admin
SQL = functools.partial(dbc.SQL, DB_URL)

notes = SQL(Notes)

#Base.metadata.create_all(engine)

async def test():
    query = {"text": "hello world"}
    # all_notes = await notes.filter_by(search=query, page=1, limit=100, sort_by="-id")
    # all_notes = await notes.create({"text": "hello world"})
    # all_notes = await notes.get_by(text="hola")
    query = (
        notes.where("name", "contains", "jane")
        | notes.where("name", "contains", "hello")
    )
    results = await notes.find(query, page=1, limit=100)
    print(results)

asyncio.run(test())

# Register - Models
dbc.Admin.register([Notes])  # ... <All Other Models>
dbc.Admin.load()

print(dbc.Admin.types)

# print(list(filter(lambda x: not x.startswith("__"), dir(notes))))

# Core: ['Q', 'database', 'table']
# Querying: ['all', 'create', 'delete', 'detail', 'filter_by', 'find', 'find_one', 'get_by', 'id_decode', 'search', 'update']
# User-Input: ['form', 'form_update']