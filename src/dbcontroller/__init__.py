"""
    Controller for <Mongo & SQL>
    Optional: [Strawberry-GraphQL]
"""

from .manager import SQL, Mongo
from .manager.utils import Decode, Objects
from .types import Admin, Database, Form, Model

# Data-Class: < Maker >
input = Form.input
search = Form.search
crud = Form.crud
form = Form.form

# Data-Class: < Fields >
field = Form.field
filters = Form.filters

# Scalars
ID = Model.id

# Scalar: JSON
JSON = Model.json
json = Model.json

# Scalar: Text(str)
Text = Model.text
text = Model.text
