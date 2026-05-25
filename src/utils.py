import pandas as pd
from pathlib import Path

def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    """
    Validates that the DataFrame contains all required columns.
    Raises ValueError if any column is missing.
    """
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing mandatory columns: {missing}. Please check the input data.")

def assert_valid_values(df: pd.DataFrame, column: str, valid_values: set) -> None:
    """
    Checks if a specific column contains only a defined set of allowed values.
    """
    if column not in df.columns:
        return
        
    current_values = set(df[column].dropna().unique())
    if not current_values.issubset(valid_values):
        unexpected = current_values - valid_values
        raise ValueError(f"Column '{column}' contains unexpected values: {unexpected}. Expected: {valid_values}")

def ensure_path_exists(path: Path) -> None:
    """
    Ensures the parent directory of a given path exists. 
    Creates it recursively if it does not exist.
    """
    path.parent.mkdir(parents=True, exist_ok=True)