"""This module contains the class definition for the various models used in the application."""

from pydantic import BaseModel

class FileMetadata(BaseModel):
    """Representation of a file's metadata."""
    file_name: str
    file_path: str
    initial_size: int
    current_size: int
    is_deleted: bool = False
    is_converted: bool = False

    def __init__(self, **data):
        """Post-initialization to set up additional attributes."""
        data['current_size'] = data.get('initial_size', 0)
        super().__init__(**data)

    def __str__(self) -> str:
        return f"File path: {self.file_path}, Initial size: {self.initial_size}, Current size: {self.current_size}, Deleted: {self.is_deleted}, Converted: {self.is_converted}"