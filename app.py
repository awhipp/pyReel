"""Service to scan a directory and store file metadata in a SQLite database."""

# ! TODO: Add fast api to run these various functions
# ! TODO: Add tests for the various modules

import os

from models import FileMetadata
from scan import ScanDirectory
from convert import VideoProcessor

# Initialize Tables
FileMetadata.create_tables()

# Check for deleted files
files = FileMetadata.get_all_files()
for file in files:
    if not os.path.exists(file.file_path):
        file.deleted = True
        file.save()

# Scan the directory
scan = ScanDirectory()

# Save the files to the database
for file in scan.files:
    if FileMetadata.check_if_file_exists(file.file_path):
        continue

    file.save()

# Print the files
files = FileMetadata.get_all_files()
for file in files:

    print(file)

print("\nProcessing files...\n")
# Process the files
files = FileMetadata.get_files_by_converted_status(converted=False)
for file in files:
    processor = VideoProcessor(input_file=file.file_path)
    processor.process()

    file.processed = processor.processed
    file.converted = processor.converted

    if file.converted:
        file.file_path = processor.output_file
        file.file_name = os.path.basename(file.file_path)

    file.save()

# Print the files
files = FileMetadata.get_all_files()
for file in files:
    print(file)