# tests/test_convert.py

from unittest.mock import MagicMock, patch


def test_video_processor_initialization(video_processor):
    """Test VideoProcessor initialization."""
    assert video_processor.input_file == "input.mp4"
    assert video_processor.output_file == "input.temp.mkv"
    assert video_processor.input_size == 0
    assert video_processor.output_size == 0
    assert video_processor.processed is False
    assert video_processor.converted is False


@patch("utils.convert.ffmpeg.input")
def test_convert_to_h265(mock_ffmpeg_input, video_processor):
    """Test convert_to_h265 method."""
    mock_ffmpeg_input.return_value = MagicMock()

    result = video_processor.convert_to_h265()

    mock_ffmpeg_input.assert_called_once_with(video_processor.input_file)

    assert result is True


@patch("utils.convert.os.path.getsize")
@patch("utils.convert.os.remove")
@patch("utils.convert.os.rename")
def test_compare_and_replace(
    mock_os_rename,
    mock_os_remove,
    mock_getsize,
    video_processor,
):
    """Test compare_and_replace method."""
    video_processor.output_file = "output.mp4"
    video_processor.input_file = "input.mp4"

    # Simulate the condition where the new file is smaller
    mock_getsize.side_effect = [100, 50]
    video_processor.compare_and_replace()
    assert video_processor.converted is True

    # Reset the mock calls
    mock_os_remove.reset_mock()
    mock_os_rename.reset_mock()

    # Simulate the condition where the new file is not smaller
    mock_getsize.side_effect = [100, 150]
    video_processor.compare_and_replace()
    assert video_processor.converted is False
    mock_os_remove.assert_called_once_with("output.mp4")


@patch("utils.convert.VideoProcessor.convert_to_h265")
@patch("utils.convert.VideoProcessor.compare_and_replace")
def test_process(mock_compare_and_replace, mock_convert_to_h265, video_processor):
    """Test process method."""
    # Simulate successful conversion
    mock_convert_to_h265.return_value = True
    video_processor.process()
    mock_convert_to_h265.assert_called_once()
    mock_compare_and_replace.assert_called_once()

    # Reset the mock calls
    mock_convert_to_h265.reset_mock()
    mock_compare_and_replace.reset_mock()

    # Simulate failed conversion
    mock_convert_to_h265.return_value = False
    video_processor.process()
    mock_convert_to_h265.assert_called()
    mock_compare_and_replace.assert_not_called()
