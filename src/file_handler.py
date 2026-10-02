"""
file_handler.py

Module responsible for discovering and identifying supported input files
within the target directory using Python's modern pathlib module.
"""

from pathlib import Path
from typing import List, Dict, Union, Optional


class FileHandler:
    """Handles file discovery and metadata extraction for incoming data files."""

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}

    def __init__(self, input_dir: Union[str, Path]):
        """
        Initialize FileHandler with an input directory path.

        :param input_dir: Path to the directory containing files to process.
        """
        self.input_dir = Path(input_dir)

    def discover_files(self) -> List[Dict[str, Union[str, Path]]]:
        """
        Scans the input directory and identifies all supported files.

        :return: List of dictionaries containing file metadata:
                 {'path': Path, 'filename': str, 'extension': str}
        :raises FileNotFoundError: If the input directory does not exist.
        """
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory '{self.input_dir}' does not exist.")

        if not self.input_dir.is_dir():
            raise NotADirectoryError(f"Provided path '{self.input_dir}' is not a directory.")

        discovered = []

        # Iterate over all items in the input directory using pathlib
        for item in self.input_dir.iterdir():
            # Ensure it is a file and has a supported extension
            if item.is_file() and item.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                discovered.append({
                    "path": item,
                    "filename": item.name,
                    "extension": item.suffix.lower()
                })

        return discovered


if __name__ == "__main__":
    # Quick module test when executed directly
    sample_dir = Path(__file__).resolve().parent.parent / "data" / "input"
    handler = FileHandler(sample_dir)
    found_files = handler.discover_files()
    
    print(f"Discovered {len(found_files)} supported file(s) in {sample_dir}:")
    for file_info in found_files:
        print(f" - {file_info['filename']} (Type: {file_info['extension']})")
