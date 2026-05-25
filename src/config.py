from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Rutas de ENTRADA (Raw)
RAW = {
    'climbers': ROOT / "data" / "raw" / "climber_df.csv",
    'grades':   ROOT / "data" / "raw" / "grades_conversion_table.csv",
    'routes':   ROOT / "data" / "raw" / "routes_rated.csv"
}

# Rutas de SALIDA (Processed)
PROCESSED = {
    'climbers': ROOT / "data" / "processed" / "climbers_clean.csv",
    'grades':   ROOT / "data" / "processed" / "grades_clean.csv",
    'routes':   ROOT / "data" / "processed" / "routes_clean.csv"
}

# Rutas de Gráficos (Visualizations)
FIGURES = ROOT / "data" / "figures"