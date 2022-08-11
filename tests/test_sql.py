"""Test - Library
"""

import asyncio
import os
import pathlib
import sys
import sqlalchemy
from types import SimpleNamespace

def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)


# Test
from dbcontroller import SQL
from sqlalchemy import create_engine

DB_URL = 'sqlite:///data/authentication.db'
metadata = sqlalchemy.MetaData()
engine = create_engine(DB_URL, echo = True)

notes_db = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(length=100)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)


notes = SQL(DB_URL, SimpleNamespace(objects=notes_db))


async def test():
    all_notes = await notes.all()
    #all_notes = await notes.create({"text": "hola"})
    print(all_notes)

#metadata.create_all(engine)
asyncio.run(test())

