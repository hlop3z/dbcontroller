# Query **List**

For simple queries you can use a **"Query `List`"**

```python
table.query_list([
    ["status", "eq", "open"],
    "or",
    ["status", "eq", "close"],
])
```

## **Generic** Operations

| Method         | Check Column (IF)                    |
| -------------- | ------------------------------------ |
| **`eq`**       | **Equals**                           |
| **`lt`**       | **Less than**                        |
| **`le`**       | **Less than or Equal than**          |
| **`gt`**       | **Greater than**                     |
| **`ge`**       | **Greater than or Equal than**       |
| **`in`**       | **In List**                          |
| **`bt`**       | **Between** "A & B"                  |
| **`contains`** | **Custom Text Search (Ignore-Case)** |

## **SQL** (Only) Operations

| Method      | Check Column (IF)                    |
| ----------- | ------------------------------------ |
| **`like`**  | **Text Search "%" (Case-Sensitive)** |
| **`ilike`** | **Text Search "%" (Ignore-Case)**    |

## **Mongo** (Only) Operations

| Method       | Check Column (IF)                        |
| ------------ | ---------------------------------------- |
| **`regex`**  | **Text Search "regex" (Case-Sensitive)** |
| **`iregex`** | **Text Search "regex" (Ignore-Case)**    |
