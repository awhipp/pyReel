"""Sqlite interface for tracking the state of the directories and files."""

import os
import sqlite3

from models import FileMetadata

class Connector():
    """Sqlite interface for tracking the state of the directories and files."""
    
    def __init__(self, db_name: str):
        """Initializes the database connection and creates the tables if they don't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Creates the tables if they don't exist.
        
        Tables:
            files: Contains the metadata of the files (Primary key: file_path).
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                file_name TEXT,
                file_path TEXT PRIMARY KEY,
                initial_size INTEGER,
                current_size INTEGER,
                is_deleted BOOLEAN DEFAULT 0,
                is_converted BOOLEAN DEFAULT 0
            )
            """
        )
        self.conn.commit()
    
    def add_file_metadata_if_not_exists(self, file: FileMetadata):
        """Adds the file metadata to the database, ignores it if it collides."""
        self.cursor.execute(
            """
            INSERT OR IGNORE INTO files
            (file_name, file_path, initial_size, current_size)
            VALUES (?, ?, ?, ?)
            """,
            (file.file_name, file.file_path, file.initial_size, file.current_size)
        )
        self.conn.commit()   

    def update_file_size(self, file_path: str, current_size: int):
        """Updates the current size of the file in the database."""
        self.cursor.execute(
            """
            UPDATE files
            SET current_size = ?
            WHERE file_path = ?
            """,
            (current_size, file_path)
        )
        self.conn.commit()   

    def update_file_path(self, old_file_path: str, new_file_path: str):
        """Updates the file path in the database."""
        file_name = os.path.basename(new_file_path)
        self.cursor.execute(
            """
            UPDATE files
            SET file_name = ?, file_path = ?
            WHERE file_path = ?
            """,
            (file_name, new_file_path, old_file_path)
        )
        self.conn.commit()   

    def set_file_converted(self, file_path: str, converted: bool = True):
        """Sets the file as converted in the database."""
        print(f"Setting {file_path} as converted: {converted}")
        self.cursor.execute(
            """
            UPDATE files
            SET is_converted = ?
            WHERE file_path = ?
            """,
            (converted, file_path)
        )
        self.conn.commit()  

    def is_file_converted(self, file_path: str):
        """Checks if the file is already converted."""
        self.cursor.execute(
            """
            SELECT is_converted
            FROM files
            WHERE file_path = ?
            """,
            (file_path,)
        )
        is_converted = self.cursor.fetchone()[0]
        return is_converted

    def set_file_deleted(self, file_path: str, deleted: bool = True):
        """Sets the file as deleted in the database."""
        self.cursor.execute(
            """
            UPDATE files
            SET is_deleted = ?
            WHERE file_path = ?
            """,
            (deleted, file_path)
        )
        self.conn.commit()   

    def optimize_and_vacuum(self):
        """Optimizes the database and reclaims the space."""
        self.cursor.execute("VACUUM")
        self.conn.commit()   

    def get_all_files(self):
        """Returns all the files from the database."""
        self.cursor.execute("SELECT * FROM files")
        rows = self.cursor.fetchall()
        # Convert the rows to FileMetadata objects (using column names)
        rows = [FileMetadata(**dict(zip([column[0] for column in self.cursor.description], row))) for row in rows]
        return rows
    
    def file_count(self):
        """Returns the number of files in the database."""
        self.cursor.execute("SELECT COUNT(*) FROM files")
        count = self.cursor.fetchone()[0]
        return count

    def file_size_saved(self):
        """Returns the total file size saved by the conversion."""
        self.cursor.execute("SELECT SUM(initial_size - current_size) FROM files")
        saved = self.cursor.fetchone()[0]
        return saved
    
    def percentage_saved(self):
        """Returns the percentage of space saved by the conversion."""
        saved = self.file_size_saved()
        self.cursor.execute("SELECT SUM(initial_size) FROM files")
        total = self.cursor.fetchone()[0]
        return (saved / total) * 100

    def close(self):
        """Closes the database connection."""
        self.conn.close()