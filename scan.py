"""Scanning class which scans a directory and returns a list of files and metadata."""

import os
from pydantic import BaseModel
from models import FileMetadata

class ScanDirectory(BaseModel):
    """Given a directory this class scans the directory and 
    returns a list of files and metadata.
    
    Args:
        root_dir (str): The directory to scan.
        valid_extensions (list[str]): List of valid extensions to scan for.
    """

    root_dir: str
    files: list[FileMetadata] = []
    valid_extensions: list[str] = []

    def __init__(self, root_dir: str, valid_extensions: list[str] = []):
        """Post-initialization to set up additional attributes."""
        super().__init__(root_dir=root_dir, valid_extensions=valid_extensions)
        self.scan_directory()
    
    def scan_directory(self):
        """Scans the directory and returns a list of files and metadata."""
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_extension = os.path.splitext(file)
                if file_extension:
                    file_extension = file_extension[1:]

                if (
                    len(self.valid_extensions) > 0
                    and 
                    file_extension not in self.valid_extensions
                ):
                        continue

                file_size = os.path.getsize(file_path)
                self.files.append(
                    FileMetadata(
                        file_name=file_name,
                        initial_file_size=file_size,
                        file_extension=file_extension,
                        file_path=file_path
                    )
                )

    # To string
    def __str__(self):
        str_rep: str = f"Scanning directory: {self.root_dir}"
        for idx, file in enumerate(self.files):
            str_rep += f"\nFile {idx+1}: {file.file_path}"
        
        return str_rep

if __name__ == "__main__":
    # Scan the directory and print the files and metadata
    scanner = ScanDirectory(root_dir=".")
    print(scanner)