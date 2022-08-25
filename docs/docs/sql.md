# **SQL** (Alchemy)

### **SQLAlchemy** Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# URL
DATABASE_URL = "sqlite:///example.db"

# Base
Base = declarative_base()
```

### **Table** | Model

> **(Databases + Controller)**

```python
import dbcontroller as dbc
import functools

# Manager
SQL = functools.partial(dbc.SQL, DATABASE_URL)

# Model
model = dbc.Model(sql=Base)

# Types
@model.sql
class User:
    name: str
    notes: dbc.Text
    meta: dbc.JSON
    disabled: bool = False
```

### **Manager**

```python
table = SQL(User)
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
    selector = "Encoded-ID" # ["Some-ID-1", "Some-ID-2", "More-IDS..."]
    form = {
        "name": "jane doll",
    }
    results = await table.update(selector, form)
    ```

=== "Delete"

    ```python
    # Delete One
    results = await table.delete("Encoded-ID")

    # Delete Many
    results = await table.delete(["Encoded-ID-1", "Encoded-ID-2", "More-IDS..."])
    ```

### **Reading** | Querying (**One**-Record)

=== "Detail"

    ```python
    results = await table.detail("Encoded-ID")
    ```

=== "Get-By"

    ```python
    results = await table.get_by(id=1)
    ```

=== "Find-One"

    ```python
    query = table.where("name", "contains", "joe")
    results = await table.find_one(query)
    ```

### **Reading** | Querying (**Multiple**-Records)

=== "All"

    ```python
    results = await table.all()
    ```

=== "Find"

    ```python
    query = (
        table.where("name", "contains", "jane")
        | table.where("name", "contains", "joe")
    )
    results = await table.find(query, page=1, limit=100, sort_by="-id")
    ```

=== "Filter-By"

    ```python
    query = {"name": "joe doe"}
    results = await table.filter_by(search=query, page=1, limit=100, sort_by="-id")
    ```

=== "Search"

    ```python
    search_value = "j"
    columns = ["name", "notes"]
    results = await table.search(columns=columns, value=search_value, page=1, limit=100, sort_by="-id")
    ```
