"""
    Controller for <Mongo & SQL>
"""

from .manager import SQL, Mongo
from .manager.utils import Objects, ReadID
from .types import Admin, Model

Text = Model.text
JSON = Model.json


class FakeModel:
    """Fake Model for Testing"""

    def __init__(self, model):
        self.objects = model
