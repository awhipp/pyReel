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

    def __new__(cls, db_path: str = os.getenv("SQLITE_DB", "files.db")):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path: str):
        """Initializes the database connection and creates the tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        logger.info(f"Connected to database: {db_path}")

    def close(self):
        """Closes the database connection"""
        self.conn.close()
        logger.info(f"Closed database connection: {self.db_path}")

    def optimize_and_vacuum(self):
        """Optimizes the database and reclaims the space."""
        self.cursor.execute("VACUUM")
        self.conn.commit()
        logger.info(f"Database optimized and vacuumed: {self.db_path}")
