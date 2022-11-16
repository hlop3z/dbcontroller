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
import dbcontroller as dbc

sql = dbc.Controller(sql="sqlite:///example.db")
```

## Database **Controller**

```py
@sql.model(table_name="users")
class User:
    name: str
    notes: dbc.text
    meta: dbc.json
    disabled: bool = False
```

## Load Classes (**Manager**)

```py
# Init Objects
dbc.load([User])
```

## SQLAlchemy

```py
from sqlalchemy import create_engine

# Init Table (SQLAlchemy)
engine = create_engine(sql.url, echo=True)
sql.base.metadata.create_all(engine)
```

---

## Demo

---

#### **Create**

```py
await User.create([{"name": "joe doe"}, {"name": "jane doll"}])
```

#### **Get-All**

```py
await User.all()
```
