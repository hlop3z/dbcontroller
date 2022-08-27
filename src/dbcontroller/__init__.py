"""
    Controller for <Mongo & SQL>
    Optional: [Strawberry-GraphQL]
"""

from .manager import SQL, Mongo
from .manager.utils import Decode, Objects
from .types import Admin, Model, Database, dataclass, field

# Data-Class Maker
input = dataclass

# Scalars
Text = Model.text
JSON = Model.json
ID = Model.id