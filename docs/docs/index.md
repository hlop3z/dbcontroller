# Welcome to **DataBase-Controller**

### To Be Used With . . .

- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) and [Databases](https://pypi.org/project/databases/)
- [PyMongo](https://pypi.org/project/pymongo/) and [Motor](https://pypi.org/project/motor/)

## **C.U.D** Methods

| Method       | Is Used To...                | Variables          |
| ------------ | ---------------------------- | ------------------ |
| **`create`** | **Create** a Single-Records. | `(dict)`           |
| **`update`** | **Edit** Multiple-Records.   | `(list[ID], dict)` |
| **`delete`** | **Delete** Multiple-Records. | `(list[ID])`       |

## **Read (Multiple-Records)** Methods

| Method          | Is Used To...                                | Variables                                     |
| --------------- | -------------------------------------------- | --------------------------------------------- |
| **`all`**       | **All** Rows (**Multiple**-Records)          | `N/A`                                         |
| **`find`**      | **Custom-Querying** (**Multiple**-Records)   | `(query, page=1, limit=100, sort_by='-id')`   |
| **`filter_by`** | **Filter-By** Columns (**Multiple**-Records) | `(dict, page=1, etc... )`                     |
| **`search`**    | **Search** in Columns (**Multiple**-Records) | `(list[str(columns)], value, page=1, etc...)` |

## **Read (One-Record)** Methods

| Method         | Is Used To...                                         | Variables      |
| -------------- | ----------------------------------------------------- | -------------- |
| **`get_by`**   | **Filter-By** Columns (**Single**-Record)             | `(**kwargs)`   |
| **`detail`**   | Get **Details** by **GraphQL-ID** (**Single**-Record) | `(Encoded_ID)` |
| **`find_one`** | **Custom-Querying** (**Single**-Records)              | `(query)`      |

## **Util** Methods

| Method            | Is Used To...                                                                        | Variables |
| ----------------- | ------------------------------------------------------------------------------------ | --------- |
| **`form`**        | **Clean** User's **`Inputs`**. And, **only** allows fields that are in the DataBase. | `(dict)`  |
| **`form_update`** | **Clean** User's **`Inputs`**. And, **only** allows fields that are in the DataBase. | `(dict)`  |
| **`id_decode`**   | **Decode** Encoded-ID                                                                | `(str)`   |
| **`Q`**           | **Custom-Querying** for **SQLAlchemy** Tables                                        | `N/A`     |
