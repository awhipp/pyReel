""" Fixtures for the tests. """

import pytest

from utils.convert import VideoProcessor


@pytest.fixture
def video_processor():
    """Generate a VideoProcessor instance."""
    return VideoProcessor(input_file="input.mp4")
