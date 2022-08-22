"""Test - Library
"""

import asyncio
import os
import pathlib
import sys
from bson.objectid import ObjectId

def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)

# Test
import dbcontroller as dbc
import motor.motor_asyncio

# Config
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"

# Engine
ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)


# Base
Base = ENGINE[DATABASE_NAME]

# Model
Model = dbc.Model(mongo=Base)

# Types
@Model.mongo
class Notes:
    text: dbc.Text
    

# Database Admin
notes = dbc.Mongo(Notes)


async def test():
    #all_notes = await db.create({"text": "hello"})
    all_notes = await notes.all()
    #all_notes = await db.find_one({ "text" : "hola" })    
    ID = ObjectId("62f521f276a55a8fe5301684")
    all_notes = await notes.search(["text"], "h")    
    print(all_notes)

asyncio.run(test())

# Register - Models
dbc.Admin.register([Notes])
print(dbc.Admin.types)
# print(list(filter(lambda x: not x.startswith("__"), dir(db))))


# Core: ['collection', 'crud', 'table']
# Querying: ['all', 'create', 'delete', 'detail', 'filter_by', 'find', 'find_one', 'get_by', 'id_decode', 'search', 'update']
# Querying: ['all', 'create', 'delete', 'detail', 'filter_by', 'find', 'find_one', 'get_by', 'id_decode', 'search', 'update']
# User-Input: ['form', 'form_update']