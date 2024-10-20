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

__all__ = [
    "daily_close",
]

# Create a logger for this package
logger = logging.getLogger(__name__)
