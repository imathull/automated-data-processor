"""
loader.py

Module responsible for safely loading CSV, Excel, and JSON files into pandas DataFrames.
Includes error handling for corrupted, empty, or unreadable files.
"""

import json
from pathlib import Path
from typing import Union
import pandas as pd


class DataLoaderError(Exception):
    """Custom exception raised when a file fails to load."""
    pass


class DataLoader:
    """Loads supported data files into Pandas DataFrames with robust error handling."""

    @staticmethod
    def load_file(file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Main entry point for loading a file. Identifies format from extension
        and delegates to the appropriate loader method.

        :param file_path: Path object or string path to the file.
        :return: pd.DataFrame containing the raw data.
        :raises DataLoaderError: If file cannot be loaded or format is unsupported.
        """
        path = Path(file_path)

        if not path.exists():
            raise DataLoaderError(f"File not found: {path}")

        ext = path.suffix.lower()

        try:
            if ext == ".csv":
                return DataLoader._load_csv(path)
            elif ext in (".xlsx", ".xls"):
                return DataLoader._load_excel(path)
            elif ext == ".json":
                return DataLoader._load_json(path)
            else:
                raise DataLoaderError(f"Unsupported file format: '{ext}' for file {path.name}")
        except DataLoaderError:
            raise
        except Exception as e:
            raise DataLoaderError(f"Failed to load '{path.name}': {str(e)}") from e

    @staticmethod
    def _load_csv(path: Path) -> pd.DataFrame:
        """Loads CSV files into pandas DataFrame."""
        try:
            # dtype=str keeps raw values intact without premature coercion
            df = pd.read_csv(path, dtype=str, skip_blank_lines=True)
            if df.empty:
                raise DataLoaderError(f"CSV file is empty: {path.name}")
            return df
        except pd.errors.EmptyDataError:
            raise DataLoaderError(f"CSV file contains no data: {path.name}")

    @staticmethod
    def _load_excel(path: Path) -> pd.DataFrame:
        """Loads Excel files (.xlsx, .xls) into pandas DataFrame."""
        try:
            df = pd.read_excel(path, dtype=str, engine="openpyxl")
            if df.empty:
                raise DataLoaderError(f"Excel file is empty: {path.name}")
            return df
        except Exception as e:
            raise DataLoaderError(f"Error parsing Excel file {path.name}: {str(e)}")

    @staticmethod
    def _load_json(path: Path) -> pd.DataFrame:
        """Loads JSON files into pandas DataFrame."""
        try:
            # First parse JSON syntax to catch corruption early
            with open(path, "r", encoding="utf-8") as f:
                content = json.load(f)
            
            if not content:
                raise DataLoaderError(f"JSON file is empty: {path.name}")

            df = pd.DataFrame(content).astype(str)
            return df
        except json.JSONDecodeError as e:
            raise DataLoaderError(f"Invalid JSON format in {path.name}: {str(e)}")


if __name__ == "__main__":
    # Test loading sample datasets
    sample_dir = Path(__file__).resolve().parent.parent / "data" / "input"
    csv_file = sample_dir / "sales_data.csv"
    json_file = sample_dir / "sales_data.json"

    print("--- Testing CSV Loading ---")
    try:
        csv_df = DataLoader.load_file(csv_file)
        print(f"Loaded '{csv_file.name}' successfully! Shape: {csv_df.shape}")
        print(csv_df.head(3))
    except DataLoaderError as err:
        print(f"Error loading CSV: {err}")

    print("\n--- Testing JSON Loading ---")
    try:
        json_df = DataLoader.load_file(json_file)
        print(f"Loaded '{json_file.name}' successfully! Shape: {json_df.shape}")
        print(json_df.head(3))
    except DataLoaderError as err:
        print(f"Error loading JSON: {err}")
