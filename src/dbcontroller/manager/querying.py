"""
    Model Querying
"""


class Manager:
    """Class: Create a Singleton"""

    model = None

    def __new__(cls, *args, **kwargs):
        it_id = "__it__"
        it = cls.__dict__.get(it_id, None)
        if it is not None:
            return it
        it = object.__new__(cls)
        setattr(cls, it_id, it)
        it.init(*args, **kwargs)
        return it

    def init(self, *args, **kwargs):
        """Class __init__ Replacement"""

    @property
    def engine(self):
        """Return Controller"""
        return self.model.__database__

    @property
    def objects(self):
        """Return Controller"""
        return self.model.objects


def manager(cls):
    """Function: Create a Singleton"""
    custom_class = type(
        f"{cls.__name__}Manager",
        (cls, Manager),
        {},
    )
    return custom_class
