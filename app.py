"""Service to scan a directory and store file metadata in a SQLite database."""

from db import Connector
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