import pandas as pd

def _build_climber_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derives new features for climbers. 
    Assumes dates, weight, and height have been validated in cleaning.
    """
    df = df.copy()

    # 1. Time-based extraction
    date_cols = ['date_first', 'date_last']
    for col in date_cols:
        # We only check for datetime type, but we know the column exists
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            year_col_name = col.replace('date', 'year')
            df[year_col_name] = df[col].dt.year.astype('Int64')
            
            time_col_name = col.replace('date', 'time')
            if time_col_name not in df.columns:
                pos = df.columns.get_loc(col)
                df.insert(pos + 1, time_col_name, df[col].dt.time)
            
            df[col] = df[col].dt.date
    
    # 2. Years recorded calculation
    df['years_recorded'] = df['year_last'] - df['year_first']
    df = df[df['years_recorded'] >= 0] # Filter out data integrity errors

    # 3. BMI Calculation
    height_m = df['height'] / 100
    bmi = (df['weight'] / (height_m ** 2)).round(2)
    pos_weight = df.columns.get_loc('weight')
    df.insert(pos_weight + 1, 'bmi', bmi)

    return df

def _build_grades_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates reference groups and flags for climbing grades.
    """
    df = df.copy()

    # 1. Broad Level (Numeric base)
    # Extracts the first character if it's a digit (e.g., "6a+" -> "6")
    # This helps grouping all grade 6s, 7s, etc.
    broad_level = df['grade_fra'].str.extract(r'(\d)').astype('Int64')
    pos_fra = df.columns.get_loc('grade_fra')
    df.insert(pos_fra + 1, 'broad_level', broad_level)

    # 2. Is Plus Flag
    # Detects if the French grade contains a "+" sign
    is_plus = df['grade_fra'].str.contains(r'\+', na=False)
    df.insert(pos_fra + 2, 'is_plus', is_plus)

    # 3. Difficulty Category
    # Categorize the IDs into 4 levels of expertise
    # Based on the typical distribution of climbing IDs (0-85 approx)
    bins = [-1, 2, 30, 51, 71, 100]
    labels = ['Unrated', 'Beginner', 'Intermediate', 'Advanced', 'Elite']
    grade_category = pd.cut(df['grade_id'], bins=bins, labels=labels, include_lowest=True)
    pos_id = df.columns.get_loc('grade_id')
    df.insert(pos_id + 1, 'grade_category', grade_category)

    return df

def _build_routes_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enhanced features for routes: handles grade mapping and categorical popularity.
    """
    df = df.copy()

    # 1. Create a Key for Merging with 'grades'
    # We round the float mean to the nearest integer to match grade_id
    df['grade_id'] = df['grade_mean'].round().astype('Int64')

    # 2. Categorical Popularity (Instead of Boolean)
    # We use quantiles to ensure we have a balanced distribution of labels
    if df['rating_tot'].nunique() > 1:
        # Define 4 levels of popularity
        df['popularity_level'] = pd.qcut(
            df['rating_tot'], 
            q=4, 
            labels=['Quiet', 'Regular', 'Highly Rated', 'Classic']
        )
    
    # 3. Sector Route Density (Same as before)
    density = df.groupby('sector')['name_id'].transform('count').astype('Int64')
    pos_sector = df.columns.get_loc('sector')
    df.insert(pos_sector + 1, 'routes_in_sector', density)

    # 4. Tall Friendly Flag (Same as before)
    is_tall = df['tall_recommend_sum'] > 0
    pos_tall = df.columns.get_loc('tall_recommend_sum')
    df.insert(pos_tall + 1, 'is_tall_friendly', is_tall)

    return df

def build_all_features(dfs: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Orchestrator for feature engineering."""
    featured_dfs = {}
    
    feature_map = {
        'climbers': _build_climber_features,
        'grades': _build_grades_features,
        'routes': _build_routes_features
    }

    for name, df in dfs.items():
        if name in feature_map:
            featured_dfs[name] = feature_map[name](df)
        else:
            featured_dfs[name] = df # No changes if no logic defined
            
    return featured_dfs



def merge_datasets(df_left: pd.DataFrame, df_right: pd.DataFrame, on_col: str) -> pd.DataFrame:
    """
    Generic project helper to merge two DataFrames on a specific column.
    Uses a left join to preserve all records from the primary (left) DataFrame.
    """
    return pd.merge(df_left, df_right, on=on_col, how='left')