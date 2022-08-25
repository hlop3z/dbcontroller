> **Fields** that **translate** from a particular type between **`Python`** , **`SQL`** and **`GraphQL`** data.

## Model **Fields**

| GraphQL        | Python (dbcontroller)   | SQLAlchemy         |
| -------------- | ----------------------- | ------------------ |
| **`ID`**       | **`dbcontroller.ID`**   | Integer            |
| **`String`**   | **`str`**               | String(length=255) |
| **`String`**   | **`dbcontroller.Text`** | Text               |
| **`Integer`**  | **`int`**               | Integer            |
| **`Float`**    | **`float`**             | Float              |
| **`Boolean`**  | **`bool`**              | Boolean            |
| **`Datetime`** | **`datetime.datetime`** | DateTime           |
| **`Date`**     | **`datetime.date`**     | Date               |
| **`Time`**     | **`datetime.time`**     | Time               |
| **`Decimal`**  | **`decimal.Decimal`**   | Decimal            |
| **`JSON`**     | **`dbcontroller.JSON`** | JSON               |

## Your **instance** includes **two** fields

1. **`_id` :** **(str)** Meant to be the **original** **`Database`** unique identifier.
2. **`id` :** **(str)** Meant to be the **client's** **`GraphQL`** unique identifier.

---

> **`ID`** is a special **Field** that represents the automatically created **`ID`** field for the database.
> You **won't use it** directly in your code.

## Python **Fields**

- **`dbcontroller.ID`**
- **`str`**
- **`dbcontroller.Text`**
- **`int`**
- **`float`**
- **`bool`**
- **`datetime.datetime`**
- **`datetime.date`**
- **`datetime.time`**
- **`datetime.Decimal`**
- **`dbcontroller.JSON`**

## Usage **Example**

```python title="types.py"
# -*- coding: utf-8 -*-
"""
    Types
"""
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

import dataclasses as dc
import datetime
import decimal
import typing

import dbcontroller as dbc

# URL
DATABASE_URL = "sqlite:///example.db"

# Base
Base = declarative_base()

# Manager
SQL = functools.partial(dbc.SQL, DATABASE_URL)

# Model
model = dbc.Model(sql=Base)


# DateTime Functions
class Date:
    datetime = lambda: datetime.datetime.now()
    date = lambda: datetime.date.today()
    time = lambda: datetime.datetime.now().time()


# Create your <types> here.
@model.sql
class Product:
    name: str
    aliases: list[str] | None = None
    stock: int | None = None
    is_available: bool | None = None
    created_on: datetime.datetime = dc.field(default_factory=Date.datetime)
    available_from: datetime.date = dc.field(default_factory=Date.date)
    same_day_shipping_before: datetime.time = dc.field(default_factory=Date.time)
    price: decimal.Decimal | None = None
    notes: list[dbc.Text] = dc.field(default_factory=list)
    is_object: dbc.JSON = dc.field(default_factory=dict)

    async def category(self) -> typing.Optional["Category"]:
        return Category(name="awesome")


@model.sql
class Category:
    name: str
```
