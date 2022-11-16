!!! info "Load"

    The **`Load`** method. Is to **initiate** the **`objects`**.

    By default the objects **do not** get initialized. The reason being that if you have **(2) two tables** that connect with each other.
    The **reference** can break if both of them are not initialized.

    Therefore, we want to initiate them **all at the same time**.

```python
dbcontroller.load([ ModelOne, ModelTwo ])
```
