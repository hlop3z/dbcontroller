!!! info "Usage"

    The **Manager** is the **interface** for **creating** database **`operations`**.
    It gives **`functionality`** at the “**Table - Level**”.

## Setup

> Create the **`Model/Type`** aka: Database "**`Table`**"

```python title="types.py"
import dbcontroller as dbc

sql = dbc.Controller(sql="sqlite:///example.db")

@sql.model
class User:
    name: str
```

> Create the **`Manager`**

```python title="manager.py"
import dbcontroller as dbc

from . import types


# (Reusable) — Base Manager
class Base:
    @classmethod
    async def all(cls):
        return await cls.objects.all()

    @classmethod
    async def reset_table(cls):
        return await cls.objects.delete(None, all=True)


# (Model | Type) — Manager
@dbc.manager
class User(Base):
    model = types.User

    @classmethod
    async def create(cls, form):
        results = await cls.objects.create(
            {
                "name": form.name,
            }
        )
        return results
```

## Testing (**Usage**)

> Test the **`Manager`**

```python title="example.py"
from .manager import User

await User.reset_table()
```
