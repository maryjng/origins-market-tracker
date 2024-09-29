import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Metadata, db
from classes.DatabaseHandler import DatabaseHandler
from test_config import DB_USER, DB_PW, DB_NAME, DB_URL

@pytest.fixture(scope='module')
def test_db():
    DB_TEST_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_URL}/{DB_NAME}"
    engine = create_engine(DB_TEST_URL)
    Session = sessionmaker(bind=engine)
    db.metadata.create_all(engine)

    session = Session()
    yield session

    db.metadata.drop_all(engine)
    session.close()
    engine.dispose()

@pytest.fixture
def db_handler(test_db):
    return DatabaseHandler(test_db)

def test_get_latest_timestamp_empty(db_handler):
    """Test get_latest_timestamp when there is no metadata in the test database."""
    assert db_handler.get_latest_timestamp() is None

def test_get_latest_timestamp_populated(db_handler):
    """Test get_latest_timestamp when there is a record in the test database."""
    # Set up the database state with a known timestamp
    db_handler.db_session.add(Metadata(latest_request_timestamp="2023-09-20 10:00:00"))
    db_handler.db_session.commit()

    # Verify that the timestamp is correctly retrieved
    assert str(db_handler.get_latest_timestamp()) == "2023-09-20 10:00:00"

def test_update_latest_timestamp(db_handler):
    """Test update_latest_timestamp works correctly."""
    db_handler.db_session.update_latest_timestamp("2023-09-21 12:00:00")
    print(db_handler.get_latest_timestamp())

    assert str(db_handler.get_latest_timestamp()) == "2023-09-21 12:00:00"


