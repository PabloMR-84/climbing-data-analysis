import pandas as pd
from src.config import RAW, PROCESSED
from src.utils import ensure_path_exists

def load_data(dataset_name: str) -> pd.DataFrame:
    """
    Reads a single CSV file from the RAW configuration with error handling.
    """
    path = RAW.get(dataset_name)
    if path is None or not path.exists():
        print(f"Warning: Dataset '{dataset_name}' not found at {path}.")
        return None
    
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Error loading {dataset_name}: {e}")
        return None

def load_all_raw_data() -> dict[str, pd.DataFrame]:
    """
    Loads all datasets defined in the RAW config into a dictionary of DataFrames.
    """
    dfs = {name: load_data(name) for name in RAW.keys()}
    # Filter out failed loads
    return {name: df for name, df in dfs.items() if df is not None}

def save_data(df: pd.DataFrame, dataset_name: str) -> None:
    """
    Saves a single DataFrame to the PROCESSED folder.
    """
    path = PROCESSED.get(dataset_name)
    if path:
        ensure_path_exists(path)
        df.to_csv(path, index=False)
        print(f"File saved: {path.name}")

def save_all_processed_data(dfs: dict[str, pd.DataFrame]) -> None:
    """
    Saves a dictionary of cleaned DataFrames to the PROCESSED folder.
    """
    for name, df in dfs.items():
        save_data(df, name)