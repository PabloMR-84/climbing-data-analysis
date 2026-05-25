from pathlib import Path

# Define the base directory of the project (two levels up from this file)
ROOT = Path(__file__).resolve().parent.parent

# INPUT Data Paths (Raw source files)
# These are the original, uncleaned datasets
RAW = {
    'climbers': ROOT / "data" / "raw" / "climber_df.csv",
    'grades':   ROOT / "data" / "raw" / "grades_conversion_table.csv",
    'routes':   ROOT / "data" / "raw" / "routes_rated.csv"
}

# OUTPUT Data Paths (Processed files)
# These are the standardized files generated after the cleaning pipeline
PROCESSED = {
    'climbers': ROOT / "data" / "processed" / "climbers_clean.csv",
    'grades':   ROOT / "data" / "processed" / "grades_clean.csv",
    'routes':   ROOT / "data" / "processed" / "routes_clean.csv"
}

# Visualization Export Path
# Directory where all generated plots and charts will be saved
FIGURES = ROOT / "data" / "figures"