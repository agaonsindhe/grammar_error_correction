import os


def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """
    Check if the file extension is allowed.

    Args:
        filename (str): Name of the uploaded file.
        allowed_extensions (set): Set of allowed file extensions.

    Returns:
        bool: True if the file is allowed, False otherwise.
    """
    print(f"allowed ",filename)
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_corrected_file(file_content: str, original_filename: str, upload_folder: str) -> str:
    """
    Save the corrected content to a file.

    Args:
        file_content (str): Corrected content.
        original_filename (str): Name of the original file.
        upload_folder (str): Path to the upload folder.

    Returns:
        str: Path to the saved corrected file.
    """

    corrected_filename = original_filename.replace(".txt", "_corrected.txt")
    corrected_filepath = os.path.join(upload_folder, corrected_filename)
    print(f"corrected file path ", corrected_filepath)
    print(f"corrected abs file path ", os.path.abspath(corrected_filepath))
    with open(corrected_filepath, "w") as f:
        f.write(file_content)
    return corrected_filepath


