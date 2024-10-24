"""
HistoricalPrice

Examples:
"""

__version__ = "0.2.0"
__description__ = "Wrapper around historical price APIs"
__author__ = "David McKim"
__author_email__ = "davidmckim@gmail.com"
__copyright__ = "Copyright David McKim"

import logging

from .api import daily_close
from .api_polygon import PolygonV1

__all__ = [
    "daily_close",
    "PolygonV1",
]

# Create a logger for this package
logger = logging.getLogger(__name__)
