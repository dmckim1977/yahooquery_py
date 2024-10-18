"""
Default package

Examples:
"""

__version__ = "0.1.0"
__description__ = "Project description"
__author__ = "David McKim"
__author_email__ = "davidmckim@gmail.com"
__copyright__ = "Copyright David McKim"

import logging
import os

import sentry_sdk

from dotenv import load_dotenv

from .utils import upload_to_spaces, date_encoded_filename

load_dotenv()

from .database import (
    BaseAPI,
    BaseTSDB,
    apiSessionLocal,
    tsdbSessionLocal,
    api_engine,
    tsdb_engine,
    get_api_db,
    get_tsdb_db,
    ExpectedMove,
    ExpectedMoveBase,
    ExpectedMoveCreate,
    ExpectedMoveSchema,
    save_expected_move,
    insert_dataframe_to_postgres,
)

__all__ = [

]

# Configure logging for the package
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for this package
logger = logging.getLogger(__name__)

# Create tables
logger.info("Ensuring database tables exist...")
BaseAPI.metadata.create_all(bind=api_engine)
BaseTSDB.metadata.create_all(bind=tsdb_engine)
logger.info("Database tables check complete.")

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
