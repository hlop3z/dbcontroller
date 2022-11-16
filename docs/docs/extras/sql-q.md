# SQL ( **Q** )

!!! warning "table"

    **`table`** is short for **`Model.objects`**

## Methods

!!! info "Querying"

    Simplified **SQL** Querying

### Where

```python
table.Q.where("id", "in", [1, 2, 3])
```

### Filter-By

> **`WHERE id = 1 AND name = "spongebob" AND last_name = "squarepants"`**

```python
table.Q.filter_by(id=1, name="spongebob", last_name="squarepants")
```

### Search

> **`WHERE name = "bob" OR name = "bob"`**

```python
table.Q.search(["name", "nickname"], "bob")
```

---

## Compile

!!! info "Compiling"

    **Compiling** the Query.

### Normal (**Select**)

```python
# Query
query = table.Q.search(["name", "title"], "bob")

# Compile
table.Q.select(query)
```

### Pagination (**Find**)

```python
# Query
query = table.Q.filter_by(name="bob")

# Compile
table.Q.find(
    query,          # The Query
    page    = 1,    # Current Page
    limit   = 100,  # Items Per Page
    sort_by = '-id' # Sort-By "X" Column
)
```
