# Welcome to **DataBase-Controller (DBC)**

> **C.R.U.D — Operations**. Designed to work with <a href="https://pypi.org/project/fastberry/" target="_blank">**`Fastberry`**</a>.
> But at the same time you can use the **"database-controller"** by itself as a **Standalone** tool.

## **Built** With:

| Core                                                                                | Tool                                                                              |
| ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| <a href="https://pypi.org/project/SQLAlchemy/" target="_blank">**`SQLAlchemy`**</a> | <a href="https://pypi.org/project/databases/" target="_blank">**`Databases`**</a> |
| <a href="https://pypi.org/project/pymongo/" target="_blank">**`PyMongo`**</a>       | <a href="https://pypi.org/project/motor/" target="_blank">**`Motor`**</a>         |

## **C.U.D** Methods

| Method       | Is Used To...                       | Variables              |
| ------------ | ----------------------------------- | ---------------------- |
| **`create`** | **Create** Single/Multiple Records. | `(dict or list[dict])` |
| **`update`** | **Edit** Single/Multiple Records.   | `(list[ID], dict)`     |
| **`delete`** | **Delete** Single/Multiple Records. | `(list[ID])`           |

## **Read (Multiple-Records)** Methods

| Method          | Is Used To...                                | Variables                                    |
| --------------- | -------------------------------------------- | -------------------------------------------- |
| **`all`**       | **All** Rows (**Multiple**-Records)          | `N/A`                                        |
| **`find`**      | **Custom-Querying** (**Multiple**-Records)   | `(query, page=1, limit=100, sort_by='-id')`  |
| **`filter_by`** | **Filter-By** Columns (**Multiple**-Records) | `(dict, page=1, etc... )`                    |
| **`search`**    | **Search** in Columns (**Multiple**-Records) | `(list[str(column)], value, page=1, etc...)` |

## **Read (One-Record)** Methods

| Method         | Is Used To...                                         | Variables      |
| -------------- | ----------------------------------------------------- | -------------- |
| **`get_by`**   | **Filter-By** Columns (**Single**-Record)             | `(**kwargs)`   |
| **`detail`**   | Get **Details** by **Encoded-ID** (**Single**-Record) | `(Encoded_ID)` |
| **`find_one`** | **Custom-Querying** (**Single**-Records)              | `(query)`      |

## **Util** Methods

| Method            | Is Used To...                                                                        | Variables |
| ----------------- | ------------------------------------------------------------------------------------ | --------- |
| **`form`**        | **Clean** User's **`Inputs`**. And, **only** allows fields that are in the DataBase. | `(dict)`  |
| **`form_update`** | **Clean** User's **`Inputs`**. And, **only** allows fields that are in the DataBase. | `(dict)`  |
| **`id_decode`**   | **Decode** Encoded-ID                                                                | `(str)`   |
| **`Q`**           | **Custom-Querying** for **SQLAlchemy** Tables                                        | `N/A`     |