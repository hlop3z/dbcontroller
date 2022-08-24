# **Notebook (DBC)**

## **PIP** Install

Install

```sh
python -m pip install notebook "dbcontroller[testing]"
```

Run

```sh
python -m jupyter notebook
```

## **PDM** Install

Install

```sh
pdm add notebook "dbcontroller[testing]"
```

Run

```sh
pdm run jupyter notebook
```

## Initialize

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# URL
DATABASE_URL = "sqlite:///notebook-example.db"

# Base
Base = declarative_base()

# Demo Create Tables
def create_tables():
    engine = create_engine(DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)\
```

## Database **Controller**

```py
import functools
import dbcontroller as dbc

model = dbc.Model(sql=Base)
SQL = functools.partial(dbc.SQL, DATABASE_URL)

@model.sql(table_name="users")
class User:
    name: str
    notes: dbc.Text
    meta: dbc.JSON
    disabled: bool = False
```

## Manager

```py
# Connect "Type" to "Controller"
table = SQL(User)

# Create Table
create_tables()
```

## Demo

---

#### **Create**

```py
await table.create([{"name": "joe doe"}, {"name": "jane doll"}])
```

#### **Get-All**

```py
await table.all()
```
