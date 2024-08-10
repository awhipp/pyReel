# tests/test_convert.py

from unittest.mock import MagicMock, patch

import pytest

from utils.convert import VideoProcessor


@pytest.fixture
def gen_vp():
    return VideoProcessor(input_file="input.mp4")


def test_video_processor_initialization(gen_vp):
    """Test VideoProcessor initialization."""
    assert gen_vp.input_file == "input.mp4"
    assert gen_vp.output_file == "input.temp.mkv"
    assert gen_vp.input_size == 0
    assert gen_vp.output_size == 0
    assert gen_vp.processed is False
    assert gen_vp.converted is False


@patch("utils.convert.ffmpeg.input")
def test_convert_to_h265(mock_ffmpeg_input, gen_vp):
    """Test convert_to_h265 method."""
    mock_ffmpeg_input.return_value = MagicMock()

    result = gen_vp.convert_to_h265()

    mock_ffmpeg_input.assert_called_once_with(gen_vp.input_file)

    assert result is True


@patch("utils.convert.os.path.getsize")
@patch("utils.convert.os.remove")
@patch("utils.convert.os.rename")
def test_compare_and_replace(mock_os_rename, mock_os_remove, mock_getsize, gen_vp):
    gen_vp.output_file = "output.mp4"
    gen_vp.input_file = "input.mp4"

    # Simulate the condition where the new file is smaller
    mock_getsize.side_effect = [100, 50]
    gen_vp.compare_and_replace()
    assert gen_vp.converted is True

    # Reset the mock calls
    mock_os_remove.reset_mock()
    mock_os_rename.reset_mock()

    # Simulate the condition where the new file is not smaller
    mock_getsize.side_effect = [100, 150]
    gen_vp.compare_and_replace()
    assert gen_vp.converted is False
    mock_os_remove.assert_called_once_with("output.mp4")


@pytest.mark.skip()
@patch("utils.convert.VideoProcessor.convert_to_h265")
@patch("utils.convert.VideoProcessor.compare_and_replace")
def test_process(mock_compare_and_replace, mock_convert_to_h265, gen_vp):
    # Simulate successful conversion
    mock_convert_to_h265.return_value = True
    gen_vp.process()
    mock_convert_to_h265.assert_called_once()
    mock_compare_and_replace.assert_called_once()

    # Simulate failed conversion
    mock_convert_to_h265.return_value = False
    gen_vp.process()
    mock_convert_to_h265.assert_called()
    mock_compare_and_replace.assert_not_called()
