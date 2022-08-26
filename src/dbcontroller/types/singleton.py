"""
    Object-Class Tools
"""


class Singleton:
    """Create a Singleton"""

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


class ModelSingleton(Singleton):
    """All Models"""

    def init(self):
        # BASE_DIR
        self._core_models = {}

    @property
    def types(self):
        """Types"""
        return self._core_models

    @property
    def models(self):
        """Models"""
        return self._core_models

    def register(self, all_models: list):
        """Register a Type(Model)"""
        if not isinstance(all_models, list):
            all_models = [all_models]
        # Register
        for current_type in all_models:
            self._core_models[current_type.__meta__.table_uri] = current_type

    def load(self):
        """Load Lazy-Tables"""
        for current_type in self._core_models.values():
            if current_type._lazy_object:
                if callable(current_type.objects):
                    current_type.objects()


# Admin
Admin = ModelSingleton()
