"""Sqlite interface for tracking the state of the directories and files."""

import os
import sqlite3
import threading

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
                    cls._instance = super(Connector, cls).__new__(cls)
                    cls._instance._initialize(db_path)
        return cls._instance

    def _initialize(self, db_path: str):
        """Initializes the database connection and creates the tables if they don't exist."""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        """Closes the database connection"""
        self.conn.close()

    def optimize_and_vacuum(self):
        """Optimizes the database and reclaims the space."""
        self.cursor.execute("VACUUM")
        self.conn.commit()