import pandas as pd
import re
from src.utils import assert_columns, assert_valid_values

def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes column names by converting to lowercase, stripping whitespace, 
    and replacing spaces, dots, or hyphens with underscores.
    """
    df.columns = [
        re.sub(r'[\s\.\-]+', '_', col.strip().lower()) 
        for col in df.columns
    ]
    return df

def _clean_climbers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes data types and values for the climbers dataset.
    Includes gender mapping, numeric conversion, and date parsing.
    """
    # 1. Define and validate mandatory columns
    required_cols = [
        'user_id', 'country', 'sex', 'height', 'weight', 'age', 
        'years_cl', 'date_first', 'date_last', 'grades_count', 
        'grades_first', 'grades_last', 'grades_max', 'grades_mean', 
        'year_first', 'year_last'
    ]   
    assert_columns(df, required_cols)

    # 2. Initialization and name normalization
    df = df.copy()
    df = _standardize_column_names(df)

    # 3. Validate gender codes and map to labels
    assert_valid_values(df, 'sex', {0, 1})
    gender_map = {0: 'male', 1: 'female'}
    df['sex'] = df['sex'].replace(gender_map).astype('category')

    # 4. Convert numeric columns to Nullable Integers (Int64)
    int_cols = [
        'user_id', 'age', 'height', 'weight', 'years_cl', 
        'grades_count', 'grades_first', 'grades_last', 'grades_max',
        'year_first', 'year_last'
    ]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # 5. Convert mean grades to float
    df['grades_mean'] = pd.to_numeric(df['grades_mean'], errors='coerce')

    # 6. Clean text strings and optimize as categories
    df['country'] = df['country'].astype(str).str.strip().astype('category')

    # 7. Parse date strings into datetime objects
    date_cols = ['date_first', 'date_last']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def _clean_grades(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the grades reference table by removing redundant metadata 
    and standardizing technical grade identifiers.
    """
    required_cols = ['grade_id', 'grade_fra']   
    assert_columns(df, required_cols)

    df = df.copy()
    
    # Remove automatic index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    
    df = _standardize_column_names(df)

    # Ensure IDs are integers and strip whitespace from grade strings
    df['grade_id'] = pd.to_numeric(df['grade_id'], errors='coerce').astype('Int64')
    df['grade_fra'] = df['grade_fra'].astype(str).str.strip()
    
    return df

def _clean_routes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the routes dataset, optimizing memory via categories 
    and ensuring numeric consistency for ratings and grades.
    """
    required_cols = [
        'name_id', 'country', 'crag', 'sector', 
        'name', 'tall_recommend_sum', 'grade_mean', 'cluster', 'rating_tot'
    ]
    assert_columns(df, required_cols)

    df = df.copy()
    
    # Remove automatic index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        
    df = _standardize_column_names(df)

    # Convert discrete numeric values to Int64
    int_cols = ['name_id', 'tall_recommend_sum', 'cluster']
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    # Convert continuous metrics to float
    float_cols = ['grade_mean', 'rating_tot']
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean text and convert repetitive strings to categories for efficiency
    text_cols = ['country', 'crag', 'sector', 'name']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        if col in ['country', 'crag', 'sector']:
            df[col] = df[col].astype('category')
            
    return df

# --- MASTER ORCHESTRATOR ---

def clean_all_data(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Coordinates the cleaning process for all datasets in the input dictionary.
    Performs type checking and executes specific logic for each known key.
    """
    # Validate input dictionary
    if not isinstance(dfs, dict) or not dfs:
        raise ValueError("Input 'dfs' must be a non-empty dictionary of DataFrames.")

    cleaned_dfs = {}

    # Define internal cleaning logic mapping
    cleaning_map = {
        'climbers': _clean_climbers,
        'grades': _clean_grades,
        'routes': _clean_routes
    }

    for name, df in dfs.items():
        # Verify if specific cleaning logic exists for the current dataset
        if name not in cleaning_map:
            raise KeyError(f"No cleaning logic defined for dataset: '{name}'. "
                           f"Update cleaning_map in clean_all_data() to include it.")
        
        # Type validation for the DataFrame object
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"The value for '{name}' is not a pandas DataFrame.")

        # Execute the mapped cleaning function
        cleaned_dfs[name] = cleaning_map[name](df)

    return cleaned_dfs