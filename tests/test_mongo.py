"""
    * Test - Mongo
"""

import os
import pathlib
import sys
import asyncio

def dir_up(depth):
    """Easy level-up folder(s)."""
    return sys.path.append(os.path.join(pathlib.Path(__file__).parents[depth], "src"))


# Append to (sys.path)
dir_up(1)

# Import Modules
from dbcontroller import Mongo