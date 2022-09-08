"""
    * PAGINATION
"""
from collections import namedtuple

# Page
Page = namedtuple("Page", ["offset", "limit"])


def pagination(page: int = 1, limit: int = 100):
    """[summary]
    Database Pagination.
    """
    offset = (page - 1) * limit
    return Page(offset, limit)
