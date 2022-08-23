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

=== "Find"

    ```python
    query = { "name": {"$regex": "Joe"} }
    results = await table.find(query, page=1, limit=100)
    ```
