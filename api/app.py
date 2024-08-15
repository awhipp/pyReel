"""Fast API application to process video files.

Routes:
    - /files: GET - Return a list of all files.
    - /files/check: GET - Returns a list of files that have been modified or deleted.
    - /files/scan: POST - Scan the directory and save new files.
    - /files/process: POST - Process all unconverted files.
    - /files/process/single: POST - Process a single file based on its path.
"""

import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.convert import VideoProcessor
from utils.logger import get_logger
from utils.models import FileMetadata
from utils.scan import ScanDirectory

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager to handle the lifespan of the application."""

    # Initialize tables as needed
    FileMetadata.create_tables()

    # Run application
    yield

    # Clean up any resources
    logger.debug("Shutting down the application.")


app = FastAPI(lifespan=lifespan)


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log the request and response of the API."""
    logger.debug(f"Request: {request.method} {request.url}")
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.debug(
        f"Response: {response.status_code} {request.url} completed in {process_time:.2f}s",
    )

    return response


# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ProcessSingleFileRequest(BaseModel):
    """Model for a single file to process."""

    file_path: str


class ProcessScanRequest(BaseModel):
    """Model for a directory to scan."""

    directory: str


@app.get("/files", response_model=list[FileMetadata])
def get_all_files():
    """Return a list of all files."""
    return FileMetadata.get_all_files()


@app.get("/files/check", response_model=list[FileMetadata])
def check_file_status():
    """Update files if deleted."""
    files = FileMetadata.get_all_files()
    changed_files = []
    for file in files:

        if not os.path.exists(file.file_path) and file.deleted is False:
            file.deleted = True
            file.save()
            changed_files.append(file)
            continue

        if file.deleted is False:
            file_size = os.path.getsize(file.file_path)
            if file_size != file.initial_size or file_size != file.current_size:
                file.initial_size = file_size
                file.current_size = file_size
                file.converted = False
                file.processed = False
                file.deleted = False
                changed_files.append(file)
                continue

    return changed_files


@app.post("/files/scan")
def scan_and_save_files(request: ProcessScanRequest):
    """Scan the directory and save new files."""
    logger.info(f"Scanning directory: {request}")
    scan = ScanDirectory(request.directory)

    # Save the files to the database
    for file in scan.files:
        if FileMetadata.check_if_file_exists(file.file_path):
            continue
        file.save()

    return {"message": "Directory scanned and new files saved."}


@app.post("/files/process")
def process_unconverted_files():
    """Process all unconverted files."""
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
    return {"message": "All unconverted files processed."}


@app.post("/files/process/single")
def process_single_file(request: ProcessSingleFileRequest):
    """Process a single file based on its path."""
    file = FileMetadata.get_file_by_path(request.file_path)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    processor = VideoProcessor(input_file=file.file_path)
    processor.process()

    file.processed = processor.processed
    file.converted = processor.converted

    if file.converted:
        file.file_path = processor.output_file
        file.file_name = os.path.basename(file.file_path)

    file.save()
    return {"message": f"File {file.file_path} processed."}
