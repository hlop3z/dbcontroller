"""
    * Response
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    """[summary]
    Output from the database (SQL or MongoDB) response.
    """

    data: Any = None
    error: bool = False
    message: str = None
    count: int = 0
    pages: int = 0
