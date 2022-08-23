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
class User:
    name: str
    notes: dbc.Text
    meta: dbc.JSON
    disabled: bool = False


table = SQL(User)

# Create-Tables
# Base.metadata.create_all(engine)

# Register - Models
dbc.Admin.register([User])  # ... <All Other Models>
dbc.Admin.load()

print(dbc.Admin.types)
