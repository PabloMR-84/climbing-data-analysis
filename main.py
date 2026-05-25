import src.io as io
import src.cleaning as cl
import src.features as ft
import src.viz as viz

def main():
    """
    Main entry point for the climbing data pipeline.
    Executes loading, cleaning, feature engineering, and visualization.
    """
    print("--- Starting Data Pipeline ---")

    # 1. Load raw datasets from the configured paths
    dfs = io.load_all_raw_data()
    
    # 2. Apply strict cleaning and standardization rules
    cleaned_dfs = cl.clean_all_data(dfs)
    
    # 3. Perform feature engineering (BMI, years recorded, categories, etc.)
    featured_dfs = ft.build_all_features(cleaned_dfs)
    
    # 4. Save the processed DataFrames to the 'data/processed' folder
    io.save_all_processed_data(featured_dfs)
    
    print("\n--- Generating Visualization Suite ---")
    
    # 5. Execute all study plots and save them into organized subfolders
    # We set show=False to run the process in the background without opening windows
    viz.run_full_visualization_suite(featured_dfs, save=True, show=False)

    print("\nProject execution finished successfully.")

if __name__ == "__main__":
    main()