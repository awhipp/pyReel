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
                file_name TEXT NOT NULL,
                initial_file_size INTEGER NOT NULL,
                file_extension TEXT,
                file_path TEXT PRIMARY KEY,
                final_file_size INTEGER
            )
            """
        )
        self.conn.commit()
    
    def add_file_metadata(self, file: FileMetadata):
        """Adds the file metadata to the database, updates it if it collides."""
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO files
            (file_name, initial_file_size, file_extension, file_path, final_file_size)
            VALUES (?, ?, ?, ?, ?)
            """,
            (file.file_name, file.initial_file_size, file.file_extension, file.file_path, file.final_file_size)
        )
        self.conn.commit()
        
    def update_file_metadata(self, file: FileMetadata):
        """Updates the file metadata in the database."""
        self.cursor.execute(
            """
            UPDATE files
            SET final_file_size = ?
            WHERE file_path = ?
            """,
            (file.final_file_size, file.file_path)
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
        return rows
    
    def file_count(self):
        """Returns the number of files in the database."""
        self.cursor.execute("SELECT COUNT(*) FROM files")
        count = self.cursor.fetchone()[0]
        return count

    def file_size_saved(self):
        """Returns the total file size saved by the conversion."""
        self.cursor.execute("SELECT SUM(initial_file_size - final_file_size) FROM files")
        saved = self.cursor.fetchone()[0]
        return saved
    
    def percentage_saved(self):
        """Returns the percentage of space saved by the conversion."""
        saved = self.file_size_saved()
        self.cursor.execute("SELECT SUM(initial_file_size) FROM files")
        total = self.cursor.fetchone()[0]
        return (saved / total) * 100

    def close(self):
        """Closes the database connection."""
        self.conn.close()


if __name__ == "__main__":
    from scan import ScanDirectory

    # Create a connector object
    connector = Connector("files.db")
    
    # Add files to the database
    scanner = ScanDirectory(root_dir=".")
    for file in scanner.files:
        connector.add_file_metadata(file)

    # Optimize
    connector.optimize_and_vacuum()
    
    # Get all files from the database
    files = connector.get_all_files()
    for file in files:
        print(file)

    # Stats
    print(f"Total files: {connector.file_count()}")
    print(f"Total size saved: {connector.file_size_saved()} bytes")
    print(f"Percentage saved: {connector.percentage_saved()}%")
    
    # Close the connection
    connector.close()