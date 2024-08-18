""" Fixtures for the tests. """

import shutil
import uuid

import cv2
import numpy as np
import pytest
from utils.convert import VideoProcessor


def create_black_video(filepath, duration=5, fps=30, width=640, height=480):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))

    # Create a black frame
    black_frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Write the black frames to the video file
    for _ in range(duration * fps):
        out.write(black_frame)

    out.release()


def generate_temp_video(file_directory):
    """Generate a temporary video file."""
    file_name = str(uuid.uuid4()) + ".mp4"
    video_path = file_directory.join(file_name)
    create_black_video(video_path)
    return video_path


def generate_temp_file(file_directory):
    """Generate a temporary file."""
    file_name = str(uuid.uuid4()) + ".txt"
    file_path = file_directory.join(file_name)
    file_path.write("This is a test file.")
    return file_path


@pytest.fixture
def temp_dir(tmpdir):
    """Generate a temporary directory."""
    yield tmpdir.mkdir("temp")
    # Remove the temporary directory and all its contents
    shutil.rmtree(tmpdir)


def create_n_files(file_directory, n=5, file_type="video"):
    """Create N files of the specified type."""
    file_paths = []
    for _ in range(n):
        if file_type == "video":
            file_path = generate_temp_video(file_directory)
        elif file_type == "non-video":
            file_path = generate_temp_file(file_directory)
        file_paths.append(str(file_path))
    return file_paths


@pytest.fixture
def generate_test_files(temp_dir) -> tuple[str, list]:
    """Generate test files in the temporary directory.

    The cases are as follows:
    1. A number of video files
    2. A number of non-video files
    3. Generate N video files and M non-video files at root and subdirectories
    """
    dirs = [temp_dir, temp_dir.mkdir("subdir")]
    file_types = ["video", "non-video"]
    files = []

    # Generate video files
    for file_type in file_types:
        for directory in dirs:
            files.extend(create_n_files(directory, n=5, file_type=file_type))

    yield str(temp_dir), files


@pytest.fixture
def video_processor():
    """Generate a VideoProcessor instance."""
    return VideoProcessor(input_file="input.mp4")
