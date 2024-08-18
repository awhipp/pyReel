"""Testing the scan method."""

from utils.scan import ScanDirectory


def test_scan_directory(generate_test_files):
    """Test the scan_directory method."""

    temp_directory, generated_files = generate_test_files

    # Scan the temporary directory
    scan = ScanDirectory(root_dir=temp_directory)

    # Check if the number of files scanned is correct
    # Half of the files are video files
    assert len(scan.get_files()) == len(generated_files) / 2

    # Check if the files are video files
    for file in scan.get_files():
        assert file.file_path in generated_files
        assert file.file_name in [f.split("/")[-1] for f in generated_files]
        assert file.initial_size > 0
        assert file.initial_size is not None
        assert file.file_path.endswith(".mp4")

    # Ensure that an extra scan does not add more files
    scan.scan_directory()

    assert len(scan.get_files()) == len(generated_files) / 2
