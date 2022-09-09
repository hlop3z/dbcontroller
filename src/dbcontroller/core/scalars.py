"""
    Scalars
"""
import dataclasses as dc
import datetime
import decimal
import types
import typing

# Strawberry
try:
    import strawberry

except ImportError:
    strawberry = None


# Custom Typing
TEXT = typing.TypeVar("TEXT", str, None)
JSON = typing.TypeVar("JSON", object, dict, list, None)
ID = typing.TypeVar("ID", str, int, None)


# Map GQL
STRAWBERRY_CORE = False
SCALAR_FIELD = types.SimpleNamespace(**{key: key for key in ["ID", "TEXT", "JSON"]})
SCALAR_FIELD.TEXT = str
SCALAR_FIELD.JSON = dict
SCALAR_FIELD.ID = str
if strawberry:
    STRAWBERRY_CORE = strawberry
    SCALAR_FIELD.JSON = strawberry.scalars.JSON
    SCALAR_FIELD.ID = strawberry.ID

# Global
SCALAR_FIELD_ID = SCALAR_FIELD.ID


@dc.dataclass(frozen=True)
class APIType:
    """API-Field-Type"""

    name: str
    python: typing.Any
    # real: typing.Any


# Core Init
Scalar = {}

# Core Values
Scalar[ID] = APIType(
    name="ID",
    python=SCALAR_FIELD.ID,
)

Scalar[TEXT] = APIType(
    name="Text",
    python=SCALAR_FIELD.TEXT,
)

Scalar[JSON] = APIType(
    name="JSON",
    python=SCALAR_FIELD.JSON,
)

Scalar[str] = APIType(
    name="String",
    python=str,
)

Scalar[int] = APIType(
    name="Integer",
    python=int,
)

Scalar[float] = APIType(
    name="Float",
    python=float,
)

Scalar[bool] = APIType(
    name="Boolean",
    python=bool,
)

Scalar[datetime.date] = APIType(
    name="Date",
    python=datetime.date,
)

Scalar[datetime.datetime] = APIType(
    name="DateTime",
    python=datetime.datetime,
)

Scalar[datetime.time] = APIType(
    name="Time",
    python=datetime.time,
)

Scalar[decimal.Decimal] = APIType(
    name="Decimal",
    python=decimal.Decimal,
)
