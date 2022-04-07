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

# Create-Tables
Base.metadata.create_all(engine)
```

### Databases + Controller

```python
from databases import Database
from dbcontroller import Sql

database = Database(DATABASE_URL)
manager = Sql(database)
```

### Table | Model

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
```

### Manager

```python
table = manager(User)
```

### C.R.U.D

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

=== "Detail (Read)"

    ```python
    results = await table.detail("Some-ID")
    ```

=== "Find-One (Read)"

    ```python
    query = table.where("id", "eq", 1)
    results = await table.find_one(query)
    ```

=== "Find (Read)"

    ```python
    query = (table.where("name", "contains", "jane") | table.where("name", "contains", "joe"))
    results = await table.find(query, page=1, limit=100)
    ```
