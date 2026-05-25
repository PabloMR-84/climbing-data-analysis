# Climbing Community & Routes Analysis

### 1) Objective
Perform a comprehensive end-to-end data analysis of the sport climbing community. The project focuses on identifying performance drivers (such as experience and BMI), analyzing gender-based skill parity, and mapping global climbing hubs through a modular data engineering pipeline.

### 2) Dataset
The data is sourced from the [Climb Dataset on Kaggle](https://www.kaggle.com/datasets/jordizar/climb-dataset). It consists of three primary files:
- **Climbers**: Profiles, physical attributes, and performance data for ~11,000 users.
- **Routes**: Technical specifications and community ratings for ~56,000 climbing routes.
- **Grades**: A reference table mapping technical IDs to the French grading system (e.g., 6a to 9b).
- **Key Variables**: `grades_max`, `bmi`, `years_recorded`, `popularity_level`, `country`.

### 3) Key Questions
- **Q1**: Does Body Mass Index (BMI) act as a decisive predictor for reaching elite climbing grades?
- **Q2**: Is there a significant performance gap between male and female climbers when technical skill is factored in?
- **Q3**: Which metric of experience is more reliable: user-declared seniority or platform-recorded activity?
- **Q4**: How is climbing infrastructure (routes) distributed globally compared to the user base?

### 4) Data Issues & Fixes
- **Temporal Corruption**: Raw files contained impossible years (e.g., year 0). 
    - *Fix*: Recalculated years directly from cleaned `datetime` objects in `src/features.py`.
- **Chronological Errors**: Instances where `date_first` was registered after `date_last`. 
    - *Fix*: Implemented a vectorized swap logic in `src/cleaning.py`.
- **Structural Noise**: Unnecessary index columns and inconsistent naming conventions. 
    - *Fix*: Automated removal of `Unnamed: 0` and regex-based standardization of column names.
- **Data Integrity**: Managed missing values via type-safe casting using Nullable `Int64`.

### 5) Pipeline
The project follows a professional modular architecture:
1. **Raw**: Initial data ingestion from `data/raw/`.
2. **Clean**: Standardization and type correction (`src/cleaning.py`).
3. **Features**: Calculation of BMI, activity spans, and popularity levels (`src/features.py`).
4. **Integration**: Joining routes with grade references using internal helpers.
5. **Viz**: Automatic generation of visual reports into organized subfolders (`src/viz.py`).

### 6) Key Findings
- **Experience over Physique**: Platform-recorded activity (`years_recorded`) is a much stronger predictor of success (r=0.52) than physical build (BMI) or declared seniority.
- **Skill-Based Equity**: Despite a male-dominated demographic (87.5%), median climbing grades are remarkably similar between sexes, supporting climbing as a skill-dominant sport.
- **Quality Hubs**: Spain and Central Europe represent the core of the ecosystem, concentrating the highest volume of "Classic" (top-rated) routes.
- **Longevity**: The elite tier (9b) shows high age diversity, featuring both teenage talents and 40+ year-old veterans.

### 7) Project Structure
```
project/
├── main.py                      # Pipeline orchestrator (runs everything)
├── data/
│   ├── raw/                     # Original CSV files
│   ├── processed/               # Cleaned datasets
│   └── figures/                 # Organized visual reports (subfolders)
├── notebooks/
│   ├── data_discovery.ipynb     # Initial data profiling
│   └── comprehensive_eda.ipynb  # Comprehensive final report
├── src/
│   ├── io.py                    # Data loading and saving
│   ├── cleaning.py              # Standardization logic
│   ├── features.py              # Engineering and Integration
│   ├── viz.py                   # Visualization suite
│   └── utils.py                 # Generic helpers and validation
├── README.md                    # Modular repository layout
├── .gitignore                   # Version control exclusions
└── requirements.txt             # Project dependencies
```

### 8) How to Run

Follow these steps to set up the environment and execute the pipeline:

1. **Clone the repository and navigate to the project folder**:
   ```bash
   git clone https://github.com/PabloMR-84/climbing-data-analysis.git
   cd climbing-data-analysis
   ```

2. **Create and activate a virtual environment**:
   - **Windows**:
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   With the virtual environment activated, run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Data**:
   Download the datasets from [Kaggle](https://www.kaggle.com/datasets/jordizar/climb-dataset) and place the raw CSV files (`climber_df.csv`, `grades_conversion_table.csv`, and `routes_rated.csv`) inside the `data/raw/` directory.

5. **Run the Pipeline**:
   Execute the full automated process (Cleaning + Features + Visualizations):
   ```bash
   python main.py
   ```

6. **Explore the Results**:
   *   **Processed Data**: Check `data/processed/` for the cleaned CSVs.
   *   **Visual Reports**: Open `data/figures/` to see the generated charts organized by study area.
   *   **Deep Dive**: Open `notebooks/comprehensive_eda.ipynb` for the step-by-step interactive analysis.