"""This module contains the class definition for the various models used in the application."""

import uuid

from pydantic import BaseModel
from db import Connector

# Static instance of the database connector
db = Connector()

class FileMetadata(BaseModel):
    """Representation of a file's metadata."""
    file_id: str = str(uuid.uuid4())
    file_name: str
    file_path: str
    initial_size: int
    current_size: int
    deleted: bool = False
    converted: bool = False
    processed: bool = False

    def __init__(self, **data):
        """Post-initialization to set up additional attributes."""
        data['current_size'] = data.get('initial_size', 0)
        super().__init__(**data)

    def __str__(self) -> str:
        return f"FileMetadata({self.file_id}, {self.file_name}, {self.file_path}, {self.initial_size}, {self.current_size}, {self.deleted}, {self.converted}, {self.processed})"
    
    def save(self):
        """Save the file metadata to the database, and on conflict, update the existing record."""
        db.cursor.execute(
            """
            INSERT OR REPLACE INTO files (file_id, file_name, file_path, initial_size, current_size, deleted, converted, processed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (self.file_id, self.file_name, self.file_path, self.initial_size, self.current_size, self.deleted, self.converted, self.processed)
        )
        db.conn.commit()
        
    @staticmethod
    def check_if_file_exists(file_path: str) -> bool:
        """Checks if the file exists in the database."""
        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM files
            WHERE file_path = ?
            """,
            (file_path,)
        )
        count = db.cursor.fetchone()[0]
        return count > 0
    
    @staticmethod
    def get_file_by_path(file_path: str):
        """Returns the file metadata by the file path."""
        db.cursor.execute(
            """
            SELECT *
            FROM files
            WHERE file_path = ?
            """,
            (file_path,)
        )
        row = db.cursor.fetchone()
        if row:
            return FileMetadata(**dict(zip([column[0] for column in db.cursor.description], row)))
        return None
    
    @staticmethod
    def get_all_files():
        """Returns all the files from the database."""
        db.cursor.execute("SELECT * FROM files")
        rows = db.cursor.fetchall()
        # Convert the rows to FileMetadata objects (using column names)
        rows = [FileMetadata(**dict(zip([column[0] for column in db.cursor.description], row))) for row in rows]
        return rows
    
    @staticmethod
    def get_files_by_converted_status(converted: bool, deleted: bool = False):
        """Returns the files based on the converted status."""
        db.cursor.execute(
            """
            SELECT *
            FROM files
            WHERE converted = ?
            AND deleted = ?
            """,
            (converted, deleted)
        )
        rows = db.cursor.fetchall()
        # Convert the rows to FileMetadata objects (using column names)
        rows = [FileMetadata(**dict(zip([column[0] for column in db.cursor.description], row))) for row in rows]
        return rows
    
    @staticmethod
    def get_files_by_processed_status(processed: bool, deleted: bool = False):
        """Returns the files based on the processed status."""
        db.cursor.execute(
            """
            SELECT *
            FROM files
            WHERE processed = ?
            AND deleted = ?
            """,
            (processed, deleted)
        )
        rows = db.cursor.fetchall()
        # Convert the rows to FileMetadata objects (using column names)
        rows = [FileMetadata(**dict(zip([column[0] for column in db.cursor.description], row))) for row in rows]
        return rows

    @staticmethod
    def get_count():
        """Returns the number of files in the database."""
        db.cursor.execute("SELECT COUNT(1) FROM files")
        count = db.cursor.fetchone()[0]
        return count

    @staticmethod
    def file_size_saved():
        """Returns the total file size saved by the conversion."""
        db.cursor.execute("SELECT SUM(initial_size - current_size) FROM files")
        saved = db.cursor.fetchone()[0]
        return saved
    
    @staticmethod
    def percentage_saved():
        """Returns the percentage of space saved by the conversion."""
        saved = FileMetadata.file_size_saved()
        db.cursor.execute("SELECT SUM(initial_size) FROM files")
        total = db.cursor.fetchone()[0]
        return (saved / total) * 100

    @staticmethod
    def create_tables():
        """Creates the tables if they don't exist, based on the FileMetadata model."""

        # Uses the FileMetadata model to create a schema dict for the table creation
        schema = FileMetadata.model_json_schema()

        ddl: str = f"""
        CREATE TABLE IF NOT EXISTS files (
            {', '.join([f"{column} {schema['properties'][column]['type']}" for column in schema['properties'].keys()])}
        )
        """

        # Set file_id as the primary key
        ddl = ddl.replace('file_id string', 'file_id string PRIMARY KEY')
        
        db.cursor.execute(ddl)
        db.conn.commit()

