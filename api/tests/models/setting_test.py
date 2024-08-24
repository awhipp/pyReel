"""Test the Setting model."""

from models.setting import Setting
from utils.db import Connector


def test_create_tables():
    """Test the creation of the tables."""
    Setting.create_tables()

    test_setting = Setting(key="key", value="value")

    test_setting.save()

    settings = Setting.get_settings()
    assert settings is not None
    assert len(settings) == 1
    assert settings[0]["key"] == "key"
    assert settings[0]["value"] == "value"

    # Check if the table was created using a describe
    db = Connector()
    cursor = db.execute("PRAGMA table_info('settings')")
    fetch = cursor.fetchall()
    assert fetch is not None
    assert len(fetch) == 2
    assert fetch[0][1] == "key"
    assert fetch[0][2] == "string"
    assert fetch[1][1] == "value"
    assert fetch[1][2] == "string"
