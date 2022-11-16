> **Fields** that **translate** from a particular type between **`Python`** , **`SQL`** and **`GraphQL`** data.

## Model **Fields**

| GraphQL        | Python (dbcontroller)      | SQLAlchemy         |
| -------------- | -------------------------- | ------------------ |
| **`ID`**       | **`dbcontroller.ID`**      | Integer            |
| **`String`**   | **`str`**                  | String(length=255) |
| **`String`**   | **`dbcontroller.text`**    | Text               |
| **`Integer`**  | **`int`**                  | Integer            |
| **`Float`**    | **`float`**                | Float              |
| **`Boolean`**  | **`bool`**                 | Boolean            |
| **`Datetime`** | **`datetime.datetime`**    | DateTime           |
| **`Date`**     | **`datetime.date`**        | Date               |
| **`Time`**     | **`datetime.time`**        | Time               |
| **`Decimal`**  | **`dbcontroller.decimal`** | String(length=255) |
| **`JSON`**     | **`dbcontroller.json`**    | JSON               |

## Your **instance** includes **two** fields

1. **`_id` :** **(str)** Meant to be the **original** **`Database`** unique identifier.
2. **`id` :** **(str)** Meant to be the **client's** **`GraphQL`** unique identifier.

---

## Usage **Example**

### Step **1**

```python title="Basic Tools"
# -*- coding: utf-8 -*-
"""
    Type | Model
"""
import dbcontroller as dbc
from typing import Optional

sql   = dbc.Controller(sql="sqlite:///example.db")
mongo = dbc.Controller(mongo="mongodb://localhost:27017/example")

# DateTime Functions
class Date:
    datetime = lambda: datetime.datetime.now()
    date = lambda: datetime.date.today()
    time = lambda: datetime.datetime.now().time()
```

### Step **2**

```python title="Create Model(s)"
@sql.model
class Product:
    # Core { Python }
    name: str | None = None
    aliases: list[str] | None = None
    stock: int | None = None
    is_available: bool | None = None

    # Custom Scalars { GraphQL }
    created_on: dbc.datetime = dbc.field(Date.datetime)
    available_from: dbc.date = dbc.field(Date.date)
    same_day_shipping_before: dbc.time = dbc.field(Date.time)
    price: dbc.decimal | None = None
    notes: list[dbc.text] = dbc.field(list)
    is_object: dbc.json = dbc.field(dict)

    # Other { Type | Model }
    category: Optional["Category"] = None

    # Other { Type | Model }
    async def group(self) -> Optional["Group"]:
        """Group Type"""
        return Group(name="awesome")

@sql.model
class Category:
    name: str

@mongo.model
class Group:
    name: str
```

### Step **3** (**SQL** Only)

```python title="Create Database's Table"
from sqlalchemy import create_engine

engine = create_engine(sql.url, echo=True)
sql.base.metadata.create_all(engine)
```
