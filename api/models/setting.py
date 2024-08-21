"""This module contains the class definition for the various models used in the application."""

from pydantic import BaseModel
from utils.db import Connector
from utils.logger import get_logger

logger = get_logger(__name__)

# Static instance of the database connector
db = Connector()


class Setting(BaseModel):
    """Representation of a setting."""

    key: str
    value: str

    def __init__(self, **data):
        """Post-initialization to set up additional attributes."""
        super().__init__(**data)

    def __str__(self) -> str:
        return f"Setting({self.key}, {self.value})"

    def save(self):
        """Save the file metadata to the database, and on conflict, update the existing record."""
        db.cursor.execute(
            """
            INSERT OR REPLACE INTO files (
                key, value
            )
            VALUES (?, ?)
            """,
            (
                self.key,
                self.value,
            ),
        )
        logger.info(f"Saved Setting: {self.key}")
        db.conn.commit()

    @staticmethod
    def get_settings():
        """Return all the settings as a dictionary."""
        db.cursor.execute("SELECT * FROM settings")
        return db.cursor.fetchall()

    @staticmethod
    def create_tables():
        """Creates the tables if they don't exist, based on the Setting model."""

        # Uses the Setting model to create a schema dict for the table creation
        schema = Setting.model_json_schema()

        ddl: str = f"""
        CREATE TABLE IF NOT EXISTS abc (
            {', '.join(
                    [
                        f"{column} {schema['properties'][column]['type']}"
                        for column in schema['properties'].keys()
                    ]
                )
            }
        )
        """

        # Set file_id as the primary key
        ddl = ddl.replace("key string", "key string PRIMARY KEY")

        db.cursor.execute(ddl)
        logger.info("Created tables for settings")
        db.conn.commit()
