"""Sqlite interface for tracking the state of the directories and files."""

import os
import sqlite3
import threading

from utils.logger import get_logger

logger = get_logger(__name__)


class Connector:
    """Sqlite interface for tracking the state of the directories and files."""

    _instance = None
    _lock = threading.Lock()

    db_path: str
    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __new__(cls, *args, **kwargs):
        """Create a singleton instance of the class."""
        with cls._lock:
            if cls._instance is None:
                logger.info("Creating a new instance of the database connector.")
                cls._instance = super().__new__(cls)
                cls._instance._initialize()

            # If connection is closed then reinitialize
            elif cls._instance.conn is None:
                logger.info("Reinitializing the database connection.")
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initializes the database connection and creates the tables if they don't exist."""
        self.db_path = os.getenv("DB_PATH", ":memory:")
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        logger.info(f"Connected to database: {self.db_path}")

    def execute(self, sql: str, params: tuple = ()):
        """Executes the sql query."""
        self.cursor.execute(sql, params)
        self.conn.commit()
        logger.debug(f"Executed sql: {sql}")
        return self.cursor

    def close(self):
        """Closes the database connection"""
        self.conn.close()
        self.conn = None
        logger.info(f"Closed database connection: {self.db_path}")

    def optimize_and_vacuum(self):
        """Optimizes the database and reclaims the space."""
        self.cursor.execute("VACUUM")
        self.conn.commit()
        logger.info(f"Database optimized and vacuumed: {self.db_path}")
