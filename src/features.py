import pandas as pd

def _build_climber_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derives new information for the climbers dataset.
    Extracts temporal components, validates data integrity, and calculates physical metrics.
    """
    df = df.copy()

    # 1. Temporal Feature Extraction
    # Extract Year and Time components from parsed datetime columns
    date_cols = ['date_first', 'date_last']
    for col in date_cols:
        # Verify that the column was successfully converted to datetime during cleaning
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            # A. Overwrite/Fix the YEAR column with reliable data from the timestamp
            year_col_name = col.replace('date', 'year')
            df[year_col_name] = df[col].dt.year.astype('Int64')
            
            # B. Extract the TIME component into a new column next to the date
            time_col_name = col.replace('date', 'time')
            if time_col_name not in df.columns:
                pos = df.columns.get_loc(col)
                df.insert(pos + 1, time_col_name, df[col].dt.time)
            
            # C. Cast main column to date only (removing time) to clean the view
            df[col] = df[col].dt.date
    
    # 2. Activity Span Calculation
    # Calculate years between first and last recorded climb
    df['years_recorded'] = df['year_last'] - df['year_first']
    
    # Data Integrity Filter: Remove records where the activity span is negative (parsing errors)
    df = df[df['years_recorded'] >= 0]

    # 3. Physical Metric: BMI (Body Mass Index)
    # Formula: weight(kg) / height(m)^2
    height_m = df['height'] / 100
    bmi = (df['weight'] / (height_m ** 2)).round(2)
    
    # Insert BMI next to the weight column for better contextual grouping
    pos_weight = df.columns.get_loc('weight')
    df.insert(pos_weight + 1, 'bmi', bmi)

    return df

def _build_grades_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes and categorizes the climbing grade reference table.
    Simplifies grade strings and bins technical IDs into human-readable levels.
    """
    df = df.copy()

    # 1. Broad Level Extraction
    # Extracts the leading digit to group grades by broad difficulty (e.g., "6a+" -> 6)
    broad_level = df['grade_fra'].str.extract(r'(\d)').astype('Int64')
    pos_fra = df.columns.get_loc('grade_fra')
    df.insert(pos_fra + 1, 'broad_level', broad_level)

    # 2. Technical Flag: Is Plus
    # Boolean indicator for "plus" (+) grades which usually represent a step in difficulty
    is_plus = df['grade_fra'].str.contains(r'\+', na=False)
    df.insert(pos_fra + 2, 'is_plus', is_plus)

    # 3. Climbing Expertise Categorization
    # Map technical grade IDs into 5 qualitative levels of expertise
    bins = [-1, 2, 30, 51, 71, 100]
    labels = ['Unrated', 'Beginner', 'Intermediate', 'Advanced', 'Elite']
    grade_category = pd.cut(df['grade_id'], bins=bins, labels=labels, include_lowest=True)
    
    pos_id = df.columns.get_loc('grade_id')
    df.insert(pos_id + 1, 'grade_category', grade_category)

    return df

def _build_routes_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriches the routes dataset with relational keys and relative popularity metrics.
    """
    df = df.copy()

    # 1. Relational Key: Grade ID
    # Create an integer key by rounding the mean grade for joining with the grades table
    df['grade_id'] = df['grade_mean'].round().astype('Int64')

    # 2. Relative Popularity Levels
    # Classify routes into 4 levels based on the rating distribution (quantiles)
    if df['rating_tot'].nunique() > 1:
        df['popularity_level'] = pd.qcut(
            df['rating_tot'], 
            q=4, 
            labels=['Quiet', 'Regular', 'Highly Rated', 'Classic']
        )
    
    # 3. Sector Context: Route Density
    # Calculate how many total routes exist within the same geographical sector
    density = df.groupby('sector')['name_id'].transform('count').astype('Int64')
    pos_sector = df.columns.get_loc('sector')
    df.insert(pos_sector + 1, 'routes_in_sector', density)

    # 4. Ergonomic Attribute: Tall Friendly
    # Flag routes based on community recommendations for taller climbers
    is_tall = df['tall_recommend_sum'] > 0
    pos_tall = df.columns.get_loc('tall_recommend_sum')
    df.insert(pos_tall + 1, 'is_tall_friendly', is_tall)

    return df

# --- MASTER ORCHESTRATOR ---

def build_all_features(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """
    Maps and executes specific feature engineering logic for each dataset in the dictionary.
    """
    featured_dfs = {}
    
    # Define mapping between dictionary keys and feature functions
    feature_map = {
        'climbers': _build_climber_features,
        'grades': _build_grades_features,
        'routes': _build_routes_features
    }

    for name, df in dfs.items():
        if name in feature_map:
            featured_dfs[name] = feature_map[name](df)
        else:
            # Pass through original DataFrame if no specific logic is defined
            featured_dfs[name] = df
            
    return featured_dfs

def merge_datasets(df_left: pd.DataFrame, df_right: pd.DataFrame, on_col: str) -> pd.DataFrame:
    """
    Helper utility to perform a left-join between two DataFrames based on a shared column.
    Used primarily for integrating reference tables with transaction data.
    """
    return pd.merge(df_left, df_right, on=on_col, how='left')