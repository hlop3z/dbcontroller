# SQL (Alchemy)

### Sqlalchemy Setup

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# URL
DATABASE_URL = "sqlite:///example.db"

# Base
Base = declarative_base()

# Setup
engine = create_engine(DATABASE_URL, echo=True)
```

### Table | Model

> **(Databases + Controller)**

```python
import dbcontroller as dbc
import functools

model = dbc.Model(sql=Base)
SQL = functools.partial(dbc.SQL, DATABASE_URL)

# Types
@model.sql
class Notes:
    name: str
    text: dbc.Text
    completed: bool = False
    meta: dbc.JSON
```

### Create Tables

```python
# Create-Tables

Base.metadata.create_all(engine)
```

### Manager

```python
table = SQL(Notes)

async def test():
    created = await table.create({"text": "hello world"})
    all_notes = await table.all()
    print(created)
    print(all_notes)

```

### **C.U.D** — Examples

=== "Create"

    ```python
    form = {
        "name": "joe doe",
    }
    results = await table.create(form)
    ```

=== "Update"

    ```python
    selector = "Some-ID" # ["Some-ID-1", "Some-ID-2", "More-IDS..."]
    form = {
        "name": "jane doll",
    }
    results = await table.update(selector, form)
    ```

=== "Delete"

    ```python
    # Delete One
    results = await table.delete("Some-ID")

    # Delete Many
    results = await table.delete(["Some-ID-1", "Some-ID-2", "More-IDS..."])
    ```

### **Reading** | Querying (**Multiple**-Records)

=== "All"

    ```python
    results = await table.all()
    ```

=== "Filter-By"

    ```python
    query = {"name": "joe doe"}
    results = await table.filter_by(search=query, page=1, limit=100, sort_by="-id")
    ```

=== "Find"

    ```python
    query = (
        table.where("name", "contains", "jane")
        | table.where("name", "contains", "joe")
    )
    results = await table.find(query, page=1, limit=100)
    ```

=== "Search"

    ```python
    search_value = "john"
    columns = ["first_name", "last_name"]
    results = await table.search(columns=columns, value=search_value, page=1, limit=100, sort_by="-id")
    ```

### **Reading** | Querying (**One**-Record)

=== "Detail"

    ```python
    results = await table.detail("Some-ID")
    ```

=== "Get-By"

    ```python
    results = await table.detail("Some-ID")
    ```

=== "Find-One"

    ```python
    query = table.where("id", "eq", 1)
    results = await table.find_one(query)
    ```
