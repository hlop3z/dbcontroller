# **SQL** (Alchemy)

!!! tip "Type"

    **`Database Collection`** **=** **`GraphQL Type`**

## **Collection** | Model | Type

```python
import dbcontroller as dbc

mongo = dbc.Controller(mongo="mongodb://localhost:27017/example")

# Types
@mongo.model
class User:
    name: str
    notes: dbc.text
    meta: dbc.json
    disabled: bool = False
```

### **Manager**

```python
table = User.objects
```

### **C.U.D** — Examples

=== "Create"

    ```python
    form = {
        "name": "joe doe",
    }

    # Create One
    results = await table.create(form)

    # Create Many
    results = await table.create([{"name": "joe doe"}, {"name": "jane doll"}])
    ```

=== "Update"

    ```python
    selector = "Encoded-ID" # ["Some-ID-1", "Some-ID-2", "More-IDS..."]

    form = {
        "name": "jane doll",
    }

    # Update One or Many
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
