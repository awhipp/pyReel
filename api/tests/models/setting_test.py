import pytest
from models.setting import Setting
from utils.db import Connector


@pytest.fixture(autouse=True)
def ephemeral_db():
    """Create a new database for each test."""
    Connector._instance = None
    db = Connector(db_path=":memory:")
    yield db
    db.close()


def test_create_tables(ephemeral_db):
    """Test the creation of the tables."""
    Setting.create_tables()
    cursor = ephemeral_db.cursor

    # Check if the table was created using a describe
    cursor.execute("PRAGMA table_info('settings')")
    fetch = cursor.fetchall()
    assert fetch is not None
