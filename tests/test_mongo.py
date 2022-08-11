"""Test - Library
"""

import asyncio
import os
import pathlib
import sys
from bson.objectid import ObjectId
from types import SimpleNamespace

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

db = Mongo(SimpleNamespace(objects=my_table))

async def test():
    #all_notes = await db.create({"text": "hello"})
    all_notes = await db.all()
    #all_notes = await db.find_one({ "text" : "hola" })    
    ID = ObjectId("62f521f276a55a8fe5301684")
    all_notes = await db.search(["text"], "h")    
    print(all_notes)

asyncio.run(test())