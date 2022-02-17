# SQL Where ( Operators )

- `eq` - equals
- `ne` - not equals
- `lt` - less than
- `le` - less than or equal to
- `gt` - greater than
- `ge` - greater than or equal to
- `contains` - text contains "string-to-search"
- `like` - SQL **like** operator
- `ilike` - SQL **ignore-case like** operator
- `in` - value **in** list
- `bt` - between (x, y)

```python
table.where("column", "operator", "value")
```

> You can add an **exclamation point "`!`"** at the beginning of the operator to make it a "`not`"

---

### **Example:**

```python
# Name Equals Joe
table.where("name", "eq", "joe")

# Name Not Equals Joe
table.where("name", "!eq", "joe")
```
