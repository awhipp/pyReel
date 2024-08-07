"""Service to scan a directory and store file metadata in a SQLite database."""

import os

from db import Connector
from scan import ScanDirectory
from models import FileMetadata
from convert import VideoProcessor

# Create a connector object
connector = Connector("files.db")

# Add files to the database
scanner = ScanDirectory(root_dir=".")
for file in scanner.files:
    connector.add_file_metadata_if_not_exists(file)

# Optimize
connector.optimize_and_vacuum()

# Get all files from the database
files: list[FileMetadata] = connector.get_all_files()
for f in files:
    # Check if file still exists
    if not os.path.exists(f.file_path):
        print(f"{f.file_name} no longer exists.")
        connector.set_file_deleted(f.file_path)
        continue

    if connector.is_file_converted(f.file_path):
        print(f"{f.file_name} is already converted.")
        continue

    print(f"{f.file_name} is not converted.")
    # Convert the file
    process = VideoProcessor(f.file_path)
    process.process()

    print(process)

    if process.converted:
        connector.update_file_path(old_file_path=process.input_file, new_file_path=process.output_file)
        connector.update_file_size(process.output_file, process.output_size)
        connector.set_file_converted(process.output_file, converted=process.processed)
    else:
        connector.set_file_converted(process.input_file, converted=process.processed)

# Stats
print(f"Total files: {connector.file_count()}")
print(f"Total size saved: {connector.file_size_saved()} bytes")
print(f"Percentage saved: {connector.percentage_saved()}%")

files: list[FileMetadata] = connector.get_all_files()
for f in files:
    print(f)

# Close the connection
connector.close()
