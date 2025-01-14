import pytest
from src.utils.file_utils import allowed_file, save_corrected_file

def test_allowed_file():
    """
    Test the file extension validator.
    """
    assert allowed_file("test.txt", {"txt"}) is True
    assert allowed_file("test.pdf", {"txt"}) is False


def test_save_corrected_file(tmp_path):
    """
    Test saving corrected files.
    """
    file_content = "Corrected content"
    original_filename = "sample.txt"
    upload_folder = tmp_path  # Temporary directory provided by pytest

    saved_file_path = save_corrected_file(file_content, original_filename, upload_folder)
    assert saved_file_path.endswith("_corrected.txt")
    assert open(saved_file_path).read() == file_content
