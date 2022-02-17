# Mongo (Motor)

### Mongo Setup

```python
import motor.motor_asyncio

# URL
MONGO_URL = "mongodb://localhost:27017"

# Setup
MONGO_DB = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
```

### Mongo + Controller

```python
from dbcontroller import Mongo

mongodb = Mongo(MONGO_DB)
manager = mongodb("test_databases")
```

### Manager | Table | Collection

```python
table = manager("test_collection")
```

### C.R.U.D

=== "Create"

    ```python
    form = {
        "id": None,
        "name": "Joe Doe",
    }
    await table.create(form)
    ```

=== "Update"

    ```python
    form = {
        "id": "Some-ID", # For multiple-ids: ["Some-ID-1", "Some-ID-2"]
        "name": "Jane Doll",
    }
    await table.update(form)
    ```

=== "Delete"

    ```python
    # Delete One
    await table.delete("Some-ID")

    # Delete Many
    await table.delete(["Some-ID-1", "Some-ID-2"])
    ```

=== "Detail (Read)"

    ```python
    await table.detail("Some-ID")
    ```

=== "Find-One (Read)"

    ```python
    query = { "name": {"$regex": "Joe"} }
    await table.find_one(query)
    ```

=== "Find (Read)"

    ```python
    query = { "name": {"$regex": "Joe"} }
    await table.find(query, page=1, limit=100)
    ```
