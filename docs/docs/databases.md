# Databases **Controller** (Demo)

```python
Database(sql: str = None, mongo: str = None, fastberry: bool = False)
```

## API **INFO**

```python title="Init"
import dbcontroller as dbc

DB_URL = {
    "sql" :  "sqlite:///examples.db",
    "mongo": "mongodb://localhost:27017/examples_database"
}

app = dbc.Database(sql=DB_URL["sql"], mongo=DB_URL["mongo"], fastberry=False)
```

### Core - **Keys**

| Key                       | type     | Info                                                |
| ------------------------- | -------- | --------------------------------------------------- |
| **`base`**                | property | **`from sqlalchemy.orm import declarative_base`**   |
| **`database`**            | property | **`app.database.sql`** and **`app.database.mongo`** |
| **`model`**               | property | **`app.model.sql`** and **`app.model.mongo`**       |
| **`types`**               | property | All **Types** get loaded here                       |
| **`manage(list[types])`** | method   | Create **DB-Controllers**                           |
| **`set_fastberry(bool)`** | method   | Set **Fastberry** to **`True`** or **`False`** .    |

> For **more information** about the database engine go to <a href="https://pypi.org/project/databases/" target="_blank">**`Databases`**</a>

```python title="SQL-Database"
# SQL Database
app.database.sql
```

> For **more information** about the database engine go to <a href="https://pypi.org/project/motor/" target="_blank">**`Motor`**</a>

```python title="Mongo-Database"
# Mongo Database
app.database.mongo
```

---

## Full **Demo**

---

### **Setup**

```python
import dbcontroller as dbc

DB_URL = {
    "sql" :  "sqlite:///examples.db",
    "mongo": "mongodb://localhost:27017/examples_database"
}

database = dbc.Database(sql=DB_URL["sql"], mongo=DB_URL["mongo"])
```

### **Models**

```python
@database.model.sql
class Product:
    name: str

    async def category(self) -> "Category":
        return Category(name="awesome")


@database.model.mongo
class Category:
    name: str
```

### **SQLAlchemy** (ONLY)

> Create tables for **examples**, but for migrations and more use <a href="https://pypi.org/project/alembic/" target="_blank">**`Alembic`**</a>

```python
from sqlalchemy import create_engine

engine = create_engine(DB_URL["sql"])

database.base.metadata.create_all(engine)
```

### **Manager**

```python
manager = database.manage([Product, Category])
```

### **Mongo** Demo

```python
await manager.mongo.Category.create({ "name" : "Demo Category" })
```

### **SQL** Demo

```python
await manager.sql.Product.create({ "name" : "Demo Product" })
```
