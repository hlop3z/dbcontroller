# Mongo **Where** ( Operators )

!!! warning "table"

    **`table`** is short for **`Model.objects`**

> **Usage**: `table.where(str: "column", str: "method", Any: value)`

| Method         | Check Column (IF)                        |
| -------------- | ---------------------------------------- |
| **`eq`**       | **Equals**                               |
| **`lt`**       | **Less than**                            |
| **`le`**       | **Less than or Equal than**              |
| **`gt`**       | **Greater than**                         |
| **`ge`**       | **Greater than or Equal than**           |
| **`contains`** | **Custom Text Search (Ignore-Case)**     |
| **`regex`**    | **Text Search "regex" (Case-Sensitive)** |
| **`iregex`**   | **Text Search "regex" (Ignore-Case)**    |
| **`in`**       | **In List**                              |
| **`bt`**       | **Between** "A & B"                      |

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
