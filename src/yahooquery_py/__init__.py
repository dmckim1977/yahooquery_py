"""
Default package

Examples:
"""

__version__ = "0.1.4"
__description__ = "Wrapper around yahooquery"
__author__ = "David McKim"
__author_email__ = "davidmckim@gmail.com"
__copyright__ = "Copyright David McKim"

import logging

from .api import daily_close
from api_polygon import index_eod_ohlc, index_eod_close, stock_eod_ohlcv, stock_eod_close

__all__ = [
    "daily_close",
    "index_eod_close",
    "index_eod_ohlc",
    "stock_eod_close",
    "stock_eod_ohlcv",
]

# Create a logger for this package
logger = logging.getLogger(__name__)
