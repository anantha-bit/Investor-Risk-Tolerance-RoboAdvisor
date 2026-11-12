"""
Comprehensive Exploratory Data Analysis (EDA) Module
Generates publication-quality visualizations and statistical tables analyzing:
- Investor risk tolerance distributions
- Behavioral bias: subjective risk willingness vs revealed portfolio risk
- Demographic drivers (Age, Education, Marital Status, Occupation, Kids)
- Financial capacity (Net Worth, Household Income)
- Pre- and Post-2008 crisis risk shifts
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from preprocess_scf import load_clean_data, CORE_FEATURE_COLUMNS, TARGET_COLUMN

sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 300
})

OUT_DIR = "visualizations"
REPORT_DIR = "reports"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def run_full_eda():
    print("[EDA] Loading preprocessed SCF dataset...")
    df = load_clean_data("data")
    
    # 1. Summary Statistics Table
    print("[EDA] Generating summary statistics...")
    stats = df.describe().T
    stats['skewness'] = df.skew()
    stats['kurtosis'] = df.kurtosis()
    stats_path = os.path.join(REPORT_DIR, "eda_summary_statistics.csv")
    stats.to_csv(stats_path)
    print(f"[SAVED] {stats_path}")
    
    # Mapping human-readable labels for plotting
    plot_df = df.copy()
    plot_df['Education_Label'] = plot_df['EDCL07'].map({
        1: 'No High School', 2: 'High School', 3: 'Some College', 4: 'College Degree'
    })
    plot_df['Occupation_Label'] = plot_df['OCCAT107'].map({
        1: 'Managerial/Prof', 2: 'Tech/Sales', 3: 'Production/Craft', 4: 'Unemployed/Ret'
    })
    plot_df['Marital_Label'] = plot_df['MARRIED07'].map({
        1: 'Married', 2: 'Unmarried'
    })
    plot_df['Risk_Willingness_Label'] = plot_df['RISK07'].map({
        1: 'Substantial Risk', 2: 'Above Avg Risk', 3: 'Average Risk', 4: 'No Risk Willing'
    })
    
    # -------------------------------------------------------------
    # Plot 1: Target Variable Distribution (Linear and Log-Scale)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.histplot(plot_df['TrueRiskTol'], bins=40, kde=True, color='#1f77b4', ax=axes[0])
    axes[0].set_title('Distribution of True Risk Tolerance (Linear Scale)')
    axes[0].set_xlabel('True Risk Tolerance Score (0 - 100)')
    axes[0].set_ylabel('Number of Investors')
    median_val = plot_df['TrueRiskTol'].median()
    mean_val = plot_df['TrueRiskTol'].mean()
    axes[0].axvline(median_val, color='red', linestyle='--', label=f'Median: {median_val:.2f}')
    axes[0].axvline(mean_val, color='orange', linestyle='-', label=f'Mean: {mean_val:.2f}')
    axes[0].legend()
    
    sns.boxplot(x=plot_df['TrueRiskTol'], color='#aec7e8', ax=axes[1])
    axes[1].set_title('Boxplot & Outliers of True Risk Tolerance')
    axes[1].set_xlabel('True Risk Tolerance Score (0 - 100)')
    
    plt.tight_layout()
    p1 = os.path.join(OUT_DIR, "eda_01_target_distribution.png")
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"[SAVED] {p1}")
    
    # -------------------------------------------------------------
    # Plot 2: Correlation Heatmap
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 8))
    corr = df[CORE_FEATURE_COLUMNS + [TARGET_COLUMN]].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-0.6, vmax=0.6,
                linewidths=0.5, cbar_kws={"shrink": .8})
    plt.title('Correlation Matrix: Demographics, Financials & Risk Tolerance', pad=15)
    plt.tight_layout()
    p2 = os.path.join(OUT_DIR, "eda_02_correlation_heatmap.png")
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"[SAVED] {p2}")
    
    # -------------------------------------------------------------
    # Plot 3: Demographic Drivers (Education, Occupation, Marital, Kids)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Education
    sns.barplot(data=plot_df, x='Education_Label', y='TrueRiskTol', ci=95, palette='Blues_r', ax=axes[0, 0])
    axes[0, 0].set_title('Mean Risk Tolerance by Education Level')
    axes[0, 0].set_xlabel('Education Category')
    axes[0, 0].set_ylabel('Mean Risk Tolerance')
    axes[0, 0].tick_params(axis='x', rotation=15)
    
    # Occupation
    sns.barplot(data=plot_df, x='Occupation_Label', y='TrueRiskTol', ci=95, palette='Greens_r', ax=axes[0, 1])
    axes[0, 1].set_title('Mean Risk Tolerance by Occupation Category')
    axes[0, 1].set_xlabel('Occupation Category')
    axes[0, 1].set_ylabel('Mean Risk Tolerance')
    axes[0, 1].tick_params(axis='x', rotation=15)
    
    # Marital Status
    sns.boxplot(data=plot_df, x='Marital_Label', y='TrueRiskTol', palette='Set2', showmeans=True, ax=axes[1, 0])
    axes[1, 0].set_title('Risk Tolerance by Marital Status')
    axes[1, 0].set_xlabel('Marital Status')
    axes[1, 0].set_ylabel('Risk Tolerance')
    axes[1, 0].set_ylim(0, 50)
    
    # Kids
    kids_group = plot_df.copy()
    kids_group['Kids_Group'] = kids_group['KIDS07'].apply(lambda k: '3+' if k >= 3 else str(k))
    sns.barplot(data=kids_group, x='Kids_Group', y='TrueRiskTol', ci=95, palette='Purples_r', ax=axes[1, 1])
    axes[1, 1].set_title('Mean Risk Tolerance by Number of Kids')
    axes[1, 1].set_xlabel('Number of Dependent Children')
    axes[1, 1].set_ylabel('Mean Risk Tolerance')
    
    plt.tight_layout()
    p3 = os.path.join(OUT_DIR, "eda_03_demographics_vs_risk.png")
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"[SAVED] {p3}")
    
    # -------------------------------------------------------------
    # Plot 4: Financial Capacity (Net Worth and Income vs Risk)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    pos_nw = plot_df[plot_df['NETWORTH07'] > 1000].copy()
    pos_nw['Log_NetWorth'] = np.log10(pos_nw['NETWORTH07'])
    sns.regplot(data=pos_nw, x='Log_NetWorth', y='TrueRiskTol', scatter_kws={'alpha': 0.15, 'color': '#2ca02c'},
                line_kws={'color': 'darkgreen', 'linewidth': 2}, ax=axes[0])
    axes[0].set_title('Risk Tolerance vs Log10 Net Worth')
    axes[0].set_xlabel('Log10 Household Net Worth ($)')
    axes[0].set_ylabel('True Risk Tolerance')
    
    pos_inc = plot_df[plot_df['INCOME07'] > 1000].copy()
    pos_inc['Log_Income'] = np.log10(pos_inc['INCOME07'])
    sns.regplot(data=pos_inc, x='Log_Income', y='TrueRiskTol', scatter_kws={'alpha': 0.15, 'color': '#d62728'},
                line_kws={'color': 'darkred', 'linewidth': 2}, ax=axes[1])
    axes[1].set_title('Risk Tolerance vs Log10 Income')
    axes[1].set_xlabel('Log10 Household Income ($)')
    axes[1].set_ylabel('True Risk Tolerance')
    
    plt.tight_layout()
    p4 = os.path.join(OUT_DIR, "eda_04_financial_capacity.png")
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"[SAVED] {p4}")
    
    # -------------------------------------------------------------
    # Plot 5: Subjective Willingness vs Revealed True Risk (Behavioral Gap)
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 6))
    order = ['Substantial Risk', 'Above Avg Risk', 'Average Risk', 'No Risk Willing']
    sns.boxplot(data=plot_df, x='Risk_Willingness_Label', y='TrueRiskTol', order=order, palette='magma', showmeans=True)
    plt.title('Behavioral Gap: Subjective Survey Willingness vs Revealed Risk Tolerance', pad=15)
    plt.xlabel('Self-Reported Willingness to Take Risk (Questionnaire Category)')
    plt.ylabel('Actual Revealed True Risk Tolerance')
    plt.ylim(0, 50)
    plt.tight_layout()
    p5 = os.path.join(OUT_DIR, "eda_05_subjective_vs_revealed_risk.png")
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"[SAVED] {p5}")
    
    # -------------------------------------------------------------
    # Plot 6: Age Lifecycle Dynamics
    # -------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    plot_df['Age_Group'] = pd.cut(plot_df['AGE07'], bins=[0, 35, 45, 55, 65, 100],
                                  labels=['<35', '35-45', '46-55', '56-65', '65+'])
    sns.barplot(data=plot_df, x='Age_Group', y='TrueRiskTol', palette='rocket', ci=95)
    plt.title('Investor Risk Tolerance across Age Brackets', pad=15)
    plt.xlabel('Age Group')
    plt.ylabel('Mean Risk Tolerance Score')
    plt.tight_layout()
    p6 = os.path.join(OUT_DIR, "eda_06_age_lifecycle_dynamics.png")
    plt.savefig(p6, dpi=300)
    plt.close()
    print(f"[SAVED] {p6}")

    print("[EDA] All EDA plots and statistics successfully generated.")

if __name__ == "__main__":
    run_full_eda()
