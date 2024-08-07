"""Scanning class which scans a directory and returns a list of files and metadata."""

import os
import mimetypes

from pydantic import BaseModel
from models import FileMetadata

def is_file_a_video(file_path: str) -> bool:
    """Check if the file is a video file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")

class ScanDirectory(BaseModel):
    """Given a directory this class scans the directory and 
    returns a list of files and metadata.
    
    Args:
        root_dir (str): The directory to scan.
        valid_extensions (list[str]): List of valid extensions to scan for.
    """

    root_dir: str
    files: list[FileMetadata] = []

    def __init__(self, root_dir: str):
        """Post-initialization to set up additional attributes."""
        super().__init__(root_dir=root_dir)
        self.scan_directory()
    
    def scan_directory(self):
        """Scans the directory and returns a list of files and metadata."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)

                if not is_file_a_video(file_path):
                    continue

                file_size = os.path.getsize(file_path)
                self.files.append(
                    FileMetadata(
                        file_name=file_name,
                        file_path=file_path,
                        initial_size=file_size,
                    )
                )

    # To string
    def __str__(self):
        str_rep: str = f"Scanning directory: {self.root_dir}"
        for idx, file in enumerate(self.files):
            str_rep += f"\n{idx + 1}. {file}"
        
        return str_rep

if __name__ == "__main__":
    # Scan the directory and print the files and metadata
    scanner = ScanDirectory(root_dir=".")
    print(scanner)