import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import src.features as ft 

from src.config import FIGURES
from src.utils import ensure_path_exists

# --- Internal Helpers ---

def _save_plot(filename: str, folder: str):
    """
    Ensures the specified subfolder exists and saves the current figure 
    to the target directory.
    """
    target_dir = FIGURES / folder
    ensure_path_exists(target_dir / filename)
    
    path = target_dir / filename
    plt.savefig(path, bbox_inches='tight', dpi=300)
    print(f"Plot saved successfully at: {path}")


# --- Sex and Performance Study ---

def plot_sex_distribution(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Visualizes the gender distribution of the climber population using a pie chart.
    """
    counts = df['sex'].value_counts()
    colors = ['#3498db', '#e74c3c'] 
    explode = (0.05, 0) 
    
    plt.figure(figsize=(6, 6))
    plt.pie(
        counts, labels=counts.index, autopct='%1.1f%%',
        startangle=140, colors=colors, explode=explode,
        shadow=True, textprops={'fontsize': 12, 'fontweight': 'bold'}
    )
    plt.title('Distribution of Climbers by Sex', fontsize=14, fontweight='bold', pad=20)
    plt.axis('equal') 
    
    if save:
        _save_plot("sex_distribution_pie.png", folder="sex_performance")
    if show: plt.show()
    plt.close()

def plot_grade_evolution_by_sex(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Displays regression plots to show how maximum climbing grades evolve 
    relative to years of experience, segmented by sex.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    genders = [('male', 'red', axes[0]), ('female', 'orange', axes[1])]
    
    for sex, color, ax in genders:
        data_filtered = df[df['sex'] == sex]
        sns.regplot(
            data=data_filtered, x='years_cl', y='grades_max',
            scatter_kws={'alpha': 0.3}, line_kws={'color': color},
            ax=ax, color=color
        )
        ax.set_title(f'Grade Evolution: {sex.capitalize()}', fontsize=16, fontweight='bold', pad=15)
        ax.set_xlabel('Years Climbing', fontsize=12)
        ax.set_ylabel('Max Grade reached', fontsize=12)
        ax.set_ylim(0, 100)

    plt.tight_layout()
    if save:
        _save_plot("grade_evolution_by_sex.png", folder="sex_performance")
    if show: plt.show()
    plt.close()

def plot_grade_distribution_by_sex(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Compares the statistical spread of average grades between sexes using boxplots.
    """
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='sex', y='grades_mean', palette='pastel')
    plt.title('Average Grade Distribution by Sex', fontsize=16, fontweight='bold', pad=15)
    plt.ylabel('Average Grade reached', fontsize=12)
    plt.xlabel('Sex', fontsize=12)

    sns.despine()
    plt.tight_layout()

    if save:
        _save_plot("grade_distribution_boxplot.png", folder="sex_performance")
    if show: plt.show()
    plt.close()


# --- BMI and Physical Attributes Study ---

def plot_bmi_distribution(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Plots a histogram showing the distribution of Body Mass Index (BMI) 
    among the climber population.
    """
    data_plot = df['bmi'].dropna()
    plt.figure(figsize=(10, 6))
    plt.hist(data_plot, bins=30, color='skyblue', edgecolor='black', range=(15, 35))
    plt.title('Distribution of Climbers by BMI', fontsize=16, fontweight='bold', pad=15)
    plt.ylabel('# Climbers', fontsize=12)
    plt.xlabel('Body Mass Index (BMI)', fontsize=12)

    plt.tight_layout()
    if save:
        _save_plot("bmi_distribution_histogram.png", folder="physical_attributes")
    if show: plt.show()
    plt.close()

def plot_grade_mean_vs_bmi_density(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Generates a density heatmap to reveal clusters and trends between BMI 
    and average climbing performance.
    """
    data_plot = df.dropna(subset=['bmi', 'grades_mean'])
    plt.figure(figsize=(12, 7))
    hb = plt.hexbin(data_plot['bmi'], data_plot['grades_mean'], gridsize=50, cmap='YlGnBu', bins='log', mincnt=1, edgecolors='none')
    sns.regplot(data=data_plot, x='bmi', y='grades_mean', scatter=False, color='red', line_kws={'linewidth': 1.5, 'alpha': 0.8})
    plt.colorbar(hb, label='Log10(Number of Climbers)')
    plt.title('BMI vs Average Grade (Density Heatmap)', fontsize=16, fontweight='bold', pad=15)
    plt.xlim(15, 35); plt.ylim(0, 100)
    
    sns.despine(); plt.tight_layout()
    if save:
        _save_plot("bmi_vs_grade_density.png", folder="physical_attributes")
    if show: plt.show()
    plt.close()


# --- Geographical Study ---

def plot_climbers_by_country(df: pd.DataFrame, top_n: int = 20, save: bool = False, show: bool = True):
    """
    Displays a bar chart of the top N countries with the highest number of climbers.
    """
    counts = df['country'].value_counts().head(top_n)
    plt.figure(figsize=(12, 6))
    counts.plot(kind='bar', color='steelblue', width=0.7)
    plt.title(f'Top {top_n} Countries by Number of Climbers', fontsize=16, fontweight='bold', pad=15)
    plt.xticks(rotation=65)
    sns.despine(); plt.tight_layout()

    if save:
        _save_plot(f"climbers_by_country_top{top_n}.png", folder="geography")
    if show: plt.show()
    plt.close()

def plot_routes_by_country(df: pd.DataFrame, top_n: int = 15, save: bool = False, show: bool = True):
    """
    Displays a bar chart of the top N countries with the highest number of climbing routes.
    """
    counts = df['country'].value_counts().head(top_n)
    counts.index = counts.index.str.upper()
    plt.figure(figsize=(12, 6))
    counts.plot(kind='bar', color='steelblue', width=0.7)
    plt.title(f'Top {top_n} Countries with Highest Number of Routes', fontsize=16, fontweight='bold', pad=15)
    plt.xticks(rotation=65)
    sns.despine(); plt.tight_layout()

    if save:
        _save_plot(f"routes_by_country_top{top_n}.png", folder="geography")
    if show: plt.show()
    plt.close()


# --- Route Popularity and Rankings ---

def plot_popularity_vs_difficulty(df: pd.DataFrame, use_log: bool = False, save: bool = False, show: bool = True):
    """
    Displays the distribution of route popularity across different difficulty levels.
    """
    plot_data = df[df['grade_category'] != 'Unrated'].copy()
    plot_data['grade_category'] = plot_data['grade_category'].cat.remove_unused_categories()
    my_colors = ["#BDC3C7", "#5DADE2", "#F39C12", "#E74C3C"] 
    
    plt.figure(figsize=(12, 6))
    ax = sns.countplot(data=plot_data, x='grade_category', hue='popularity_level', palette=my_colors)
    
    title = 'Route Popularity vs Difficulty'
    suffix = "_linear"
    if use_log:
        ax.set_yscale("log"); title += ' (Log)'; suffix = "_log"
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    sns.despine(); plt.tight_layout()
    
    if save:
        _save_plot(f"popularity_vs_difficulty{suffix}.png", folder="popularity_rankings")
    if show: plt.show()
    plt.close()

def plot_popularity_comparison(routes_df: pd.DataFrame, grades_df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Orchestrates the merge between routes and grades to generate popularity plots.
    """
    df_merged = ft.merge_datasets(routes_df, grades_df, on_col='grade_id')
    plot_popularity_vs_difficulty(df_merged, use_log=False, save=save, show=show)
    plot_popularity_vs_difficulty(df_merged, use_log=True, save=save, show=show)

def plot_top_climbers_table(climbers_df: pd.DataFrame, grades_df: pd.DataFrame, top_n: int = 20, save: bool = False, show: bool = True):
    """
    Generates a styled ranking table showing the top performers in the dataset.
    """
    df_combined = pd.merge(climbers_df, grades_df, left_on='grades_max', right_on='grade_id')
    df_sorted = df_combined.sort_values(by=['grades_max', 'age'], ascending=[False, True]).head(top_n).copy()
    df_sorted.insert(0, 'Rank', range(1, len(df_sorted) + 1))
    table_data = df_sorted[['Rank', 'user_id', 'age', 'country', 'grade_fra']]

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off') 
    the_table = ax.table(cellText=table_data.values, colLabels=table_data.columns, loc='center', cellLoc='center')
    the_table.auto_set_font_size(False); the_table.set_fontsize(12); the_table.scale(1.2, 2.2)

    for (row, col), cell in the_table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white'); cell.set_facecolor('#2c3e50')
        elif row % 2 == 0: cell.set_facecolor('#f2f2f2')
    
    ax.set_title(f'Top {top_n} Climbers Ranking', fontsize=20, fontweight='bold', pad=40)
    plt.tight_layout()

    if save:
        _save_plot(f"top_{top_n}_climbers_table.png", folder="popularity_rankings")
    if show: plt.show()
    plt.close()


# --- Correlation Study ---

def plot_correlation_bmi_vs_performance(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Heatmap visualization of correlation between BMI, Age, and performance.
    """
    cols = ['bmi', 'age', 'years_cl', 'grades_count', 'grades_max', 'grades_mean']
    corr = df[cols].apply(pd.to_numeric, errors='coerce').corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", center=0, square=True)
    plt.title('Correlation: BMI & Performance (Declared)', fontsize=15, fontweight='bold', pad=20)
    plt.tight_layout()

    if save:
        _save_plot("correlation_bmi_vs_performance_declared.png", folder="correlations")
    if show: plt.show()
    plt.close()

def plot_correlation_bmi_vs_recorded(df: pd.DataFrame, save: bool = False, show: bool = True):
    """
    Heatmap visualization using platform recorded years for experience.
    """
    cols = ['bmi', 'age', 'years_recorded', 'grades_count', 'grades_max', 'grades_mean']
    corr = df[cols].apply(pd.to_numeric, errors='coerce').corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", center=0, square=True)
    plt.title('Correlation: BMI & Performance (Recorded)', fontsize=15, fontweight='bold', pad=20)
    plt.tight_layout()

    if save:
        _save_plot("correlation_bmi_vs_performance_recorded.png", folder="correlations")
    if show: plt.show()
    plt.close()


# --- MASTER ORCHESTRATOR ---

def run_full_visualization_suite(dfs: dict[str, pd.DataFrame], save: bool = True, show: bool = False):
    """
    Executes all visualization functions in the module using the provided 
    dictionary of featured DataFrames.
    """
    print("Starting full visualization suite...")
    
    # 1. Sex Study
    plot_sex_distribution(dfs['climbers'], save=save, show=show)
    plot_grade_evolution_by_sex(dfs['climbers'], save=save, show=show)
    plot_grade_distribution_by_sex(dfs['climbers'], save=save, show=show)
    
    # 2. Physical Study
    plot_bmi_distribution(dfs['climbers'], save=save, show=show)
    plot_grade_mean_vs_bmi_density(dfs['climbers'], save=save, show=show)
    
    # 3. Geo Study
    plot_climbers_by_country(dfs['climbers'], save=save, show=show)
    plot_routes_by_country(dfs['routes'], save=save, show=show)
    
    # 4. Popularity & Rankings
    plot_popularity_comparison(dfs['routes'], dfs['grades'], save=save, show=show)
    plot_top_climbers_table(dfs['climbers'], dfs['grades'], save=save, show=show)
    
    # 5. Correlations
    plot_correlation_bmi_vs_performance(dfs['climbers'], save=save, show=show)
    plot_correlation_bmi_vs_recorded(dfs['climbers'], save=save, show=show)
    
    print("Full visualization suite completed successfully.")