"""Test - Library
"""

import asyncio
import os
import pathlib
import sys

def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)

# Test
from dbcontroller import Mongo
import motor.motor_asyncio

# Config
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"

# Engine
ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


# Base
Base = ENGINE[DATABASE_NAME]

my_table = Base['my_table']

db = Mongo(my_table)

async def test():
    #all_notes = await db.create({"text": "hola"})
    all_notes = await db.all()
    print(all_notes)

asyncio.run(test())
