import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Construct the DATABASE_URL
DB_DRIVER = os.getenv("DB_DRIVER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASS", "")
API_NAME = os.getenv("DB_NAME")
TSDB_NAME = os.getenv("TSDB_NAME")

# API Database logic
API_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{API_NAME}"

api_engine = create_engine(API_URL)
apiSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=api_engine)

def get_api_db():
    db = apiSessionLocal()
    try:
        yield db
    finally:
        db.close()


# TSDB Database Logic
TSDB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TSDB_NAME}"

tsdb_engine = create_engine(TSDB_URL)
tsdbSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=tsdb_engine)


def get_tsdb_db():
    db = apiSessionLocal()
    try:
        yield db
    finally:
        db.close()