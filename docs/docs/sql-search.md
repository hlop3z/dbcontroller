# SQL Search ( Operator )

---

### **Example:**

> **First-Name** or **Last-Name** Contains **Joe**

```python
search_cols = ["first_name", "last_name"]
search_text = "Joe"
query = table.search(search_cols, search_text)
```
