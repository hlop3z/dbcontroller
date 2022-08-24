# **Mongo** (Motor)

### **Mongo** Setup

```python
import motor.motor_asyncio

# Config
DATABASE_URL = "mongodb://localhost:27017"
DATABASE_NAME = "test_database"

# Engine
ENGINE = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

# Base
Base = ENGINE[DATABASE_NAME]
```

### **Collection** | Model

> **(Motor + Controller)**

```python
import dbcontroller as dbc

model = dbc.Model(mongo=Base)

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
table = dbc.Mongo(User)
```

### **C.U.D** — Examples

=== "Create"

    ```python
    form = {
        "id": None,
        "name": "Joe Doe",
    }
    results = await table.create(form)
    ```

=== "Update"

    ```python
    form = {
        "id": "Some-ID", # For multiple-ids: ["Some-ID-1", "Some-ID-2"]
        "name": "Jane Doll",
    }
    results = await table.update(form)
    ```

=== "Delete"

    ```python
    # Delete One
    results = await table.delete("Some-ID")

    # Delete Many
    results = await table.delete(["Some-ID-1", "Some-ID-2"])
    ```

### **Reading** | Querying (**One**-Record)

=== "Detail"

    ```python
    results = await table.detail("Some-ID")
    ```

=== "Get-By"

    ```python
    results = await table.get_by(id=1)
    ```

=== "Find-One"

    ```python
    query = { "name": {"$regex": "Joe"} }
    results = await table.find_one(query)
    ```

### **Reading** | Querying (**Multiple**-Records)

=== "All"

    ```python
    results = await table.all()
    ```

=== "Find"

    ```python
    search = [{"name": {"$regex": "joe"}}, {"name": {"$regex": "jane"}}]
    query = {"$or": search}
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
