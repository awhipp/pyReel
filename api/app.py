"""Core FastAPI application to requests
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from routes import files, settings
from utils.logger import get_logger

from api.models.file import FileMetadata
from api.models.setting import Setting

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan():
    """Context manager to handle the lifespan of the application."""

    # Initialize tables as needed
    FileMetadata.create_tables()
    Setting.create_tables()

    # Run application
    yield

    # Clean up any resources
    logger.debug("Shutting down the application.")


app = FastAPI(lifespan=lifespan)
app.include_router(files.router)
app.include_router(settings.router)


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
