"""This module contains the class definition for the various models used in the application."""

from pydantic import BaseModel
from typing import Optional

class FileMetadata(BaseModel):
    """Representation of a file's metadata."""
    file_name: str
    initial_file_size: int
    file_extension: Optional[str] = ""
    file_path: str
    final_file_size: int = 0