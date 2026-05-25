import pandas as pd
import re
from src.utils import assert_columns, assert_valid_values

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to standardize column names:
    lowercase, strip whitespace, and replace spaces/dots with underscores.
    """
    df.columns = [
        re.sub(r'[\s\.\-]+', '_', col.strip().lower()) 
        for col in df.columns
    ]
    return df
    


def _clean_climbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes types and corrects values for the climbers dataset.
    Relies on assert_columns for existence of data.
    """
    # 1. Define and Validate existence
    required_cols = [
        'user_id', 'country', 'sex', 'height', 'weight', 'age', 
        'years_cl', 'date_first', 'date_last', 'grades_count', 
        'grades_first', 'grades_last', 'grades_max', 'grades_mean', 
        'year_first', 'year_last'
    ]   
    assert_columns(df, required_cols)

    # 2. Setup
    df = df.copy()
    df = _standardize_column_names(df) # Everything is now lowercase

    # 3. Validate and Map 'sex'
    assert_valid_values(df, 'sex', {0, 1})
    gender_map = {0: 'male', 1: 'female'}
    df['sex'] = df['sex'].replace(gender_map).astype('category')

    # 4. Numeric Conversions
    int_cols = [
        'user_id', 'age', 'height', 'weight', 'years_cl', 
        'grades_count', 'grades_first', 'grades_last', 'grades_max',
        'year_first', 'year_last'
    ]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    df['grades_mean'] = pd.to_numeric(df['grades_mean'], errors='coerce')

    # 5. Text Cleanup
    df['country'] = df['country'].astype(str).str.strip().astype('category')

    # 6. Date Conversion
    date_cols = ['date_first', 'date_last']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    return df



def _clean_grades(df: pd.DataFrame) -> pd.DataFrame:
    """Logic specific to the grades dataset."""
    required_cols = ['grade_id', 'grade_fra']   
    assert_columns(df, required_cols)

    df = df.copy()
    
    # Check and drop 'Unnamed: 0' specifically
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    df = _standardize_column_names(df)

    # Standardize columns (No IFs needed)
    df['grade_id'] = pd.to_numeric(df['grade_id'], errors='coerce').astype('Int64')
    df['grade_fra'] = df['grade_fra'].astype(str).str.strip()
    
    return df



def _clean_routes(df: pd.DataFrame) -> pd.DataFrame:
    """Logic specific to the routes dataset."""
    required_cols = [
        'name_id', 'country', 'crag', 'sector', 
        'name', 'tall_recommend_sum', 'grade_mean', 'cluster', 'rating_tot'
    ]
    assert_columns(df, required_cols)

    df = df.copy()
    
    # Check and drop 'Unnamed: 0' specifically
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
    df = _standardize_column_names(df)

    # 1. Integers
    int_cols = ['name_id', 'tall_recommend_sum', 'cluster']
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # 2. Floats
    float_cols = ['grade_mean', 'rating_tot']
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Text and Categories
    text_cols = ['country', 'crag', 'sector', 'name']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        # Optimize memory for repetitive strings
        if col in ['country', 'crag', 'sector']:
            df[col] = df[col].astype('category')
            
    return df


# --- MASTER FUNCTION ---

def clean_all_data(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Orchestrates cleaning with strict validation. 
    Raises errors if inputs are invalid or keys are missing logic.
    """
    # 1. Ensure input is a non-empty dictionary
    if not isinstance(dfs, dict) or not dfs:
        raise ValueError("The input 'dfs' must be a non-empty dictionary of DataFrames.")

    cleaned_dfs = {}

    # Define the mapping
    cleaning_map = {
        'climbers': _clean_climbers,
        'grades': _clean_grades,
        'routes': _clean_routes
    }

    for name, df in dfs.items():
        # 2. Check if we have logic for this key
        if name not in cleaning_map:
            raise KeyError(f"No cleaning logic defined for dataset: '{name}'. "
                           f"Update cleaning_map in clean_dfs() to include it.")
        
        # 3. Ensure the value is actually a DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"The value for '{name}' is not a pandas DataFrame.")

        # Execute cleaning
        cleaned_dfs[name] = cleaning_map[name](df)

    return cleaned_dfs