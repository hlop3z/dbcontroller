# SQL **Where** ( Operators )

> **Usage**: `table.where(str: "column", str: "method", Any: value)`

| Method         | Check Column (IF)                    |
| -------------- | ------------------------------------ |
| **`eq`**       | **Equals**                           |
| **`lt`**       | **Less than**                        |
| **`le`**       | **Less than or Equal than**          |
| **`gt`**       | **Greater than**                     |
| **`ge`**       | **Greater than or Equal than**       |
| **`contains`** | **Custom Text Search (Ignore-Case)** |
| **`like`**     | **Text Search "%" (Case-Sensitive)** |
| **`ilike`**    | **Text Search "%" (Ignore-Case)**    |
| **`in`**       | **In List**                          |
| **`bt`**       | **Between** "A & B"                  |

### API - **Demo**

```python
table.where("column", "operator", "value")
```

### **Example**

> You can add an **exclamation point "`!`"** at the beginning of the operator to make it a **"`not`"**

```python
# Name Equals Joe
table.where("name", "eq", "joe")

# Name Not Equals Joe
table.where("name", "!eq", "joe")
```

### **SQLAlchemy Style**

> You can use just the **regular** SQLAlchemy **operators** instead.

```python
# Name Equals Joe
table.c.name == "joe"
```
