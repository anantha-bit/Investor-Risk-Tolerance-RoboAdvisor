"""
Script to generate standard, production-ready Jupyter Notebooks
for EDA, Preprocessing, Benchmarking, and Portfolio Allocation.
"""

import json
import os

NOTEBOOKS_DIR = "notebooks"
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def create_notebook(cells, filepath):
    nb = {
        "cells": cells,
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.12"
            },
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"[NOTEBOOK SAVED] {filepath}")

def md_cell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in text.splitlines()]}

def code_cell(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [l + "\n" for l in code.splitlines()]}

# =============================================================================
# Notebook 1: Data Acquisition and Preprocessing
# =============================================================================
cells_nb1 = [
    md_cell("""# 1. Data Acquisition & Preprocessing
## Project: Modeling Investor Risk Tolerance & Enabling an ML-Based Robo-Advisor
**Course:** Machine Learning for Big Data (MLBD) — Mini Project, PES University  
**Authors:** Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), Chandraraj Patil (PES1UG24AM425)

---
### Objectives
1. Acquire the **Survey of Consumer Finances (SCF) 2007-2009 Panel Dataset** from the Federal Reserve Board.
2. Define and calculate **Risk-Free Assets** and **Risky Assets** for pre-crisis (2007) and post-crisis (2009).
3. Compute unadjusted and S&P 500 normalized risk tolerance.
4. Filter for **Intelligent Investors** (individuals whose risk tolerance changed by $\le 10\%$ across the crisis).
5. Extract intuitive demographic, financial, and behavioral predictor variables."""),
    code_cell("""import os
import sys
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.abspath('..'))
from src.preprocess_scf import load_clean_data, CORE_FEATURE_COLUMNS, TARGET_COLUMN

print("Libraries imported successfully.")"""),
    md_cell("""### 1.1 Load and Inspect the Preprocessed SCF Data"""),
    code_cell("""df = load_clean_data('../data')
print(f"Dataset shape: {df.shape[0]} observations, {df.shape[1]} features")
df.head(10)"""),
    md_cell("""### 1.2 Inspect Ground Truth Target: TrueRiskTol"""),
    code_cell("""print("Descriptive statistics of TrueRiskTol:")
df['TrueRiskTol'].describe()"""),
    md_cell("""### 1.3 Verify Missing Values and Data Types"""),
    code_cell("""print("Missing values per column:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)""")
]
create_notebook(cells_nb1, os.path.join(NOTEBOOKS_DIR, "01_Data_Acquisition_and_Preprocessing.ipynb"))

# =============================================================================
# Notebook 2: Exploratory Data Analysis (EDA)
# =============================================================================
cells_nb2 = [
    md_cell("""# 2. Exploratory Data Analysis (EDA)
## Project: Modeling Investor Risk Tolerance & Enabling an ML-Based Robo-Advisor
**Course:** Machine Learning for Big Data (MLBD) — Mini Project, PES University  
**Authors:** Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), Chandraraj Patil (PES1UG24AM425)

---
### Key Inquiries
1. What is the distribution of investor risk tolerance?
2. How does self-reported risk willingness correlate with actual revealed portfolio risk?
3. Which demographic and financial attributes exert the strongest predictive influence?
4. What are the behavioral shifts induced by the 2008 Great Financial Crisis?"""),
    code_cell("""import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.abspath('..'))
from src.preprocess_scf import load_clean_data

df = load_clean_data('../data')
sns.set_theme(style="whitegrid")"""),
    md_cell("""### 2.1 Distribution of True Risk Tolerance"""),
    code_cell("""plt.figure(figsize=(10, 5))
sns.histplot(df['TrueRiskTol'], bins=40, kde=True, color='#1f77b4')
plt.title("Distribution of True Risk Tolerance (Revealed Metric)", fontsize=14)
plt.xlabel("Risk Tolerance Score (0 to 100)")
plt.ylabel("Frequency")
plt.axvline(df['TrueRiskTol'].mean(), color='red', linestyle='--', label=f"Mean: {df['TrueRiskTol'].mean():.2f}")
plt.axvline(df['TrueRiskTol'].median(), color='orange', linestyle='-', label=f"Median: {df['TrueRiskTol'].median():.2f}")
plt.legend()
plt.show()"""),
    md_cell("""### 2.2 Correlation Matrix Heatmap"""),
    code_cell("""plt.figure(figsize=(10, 8))
corr = df.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-0.6, vmax=0.6, linewidths=0.5)
plt.title("Correlation Matrix of Demographics, Financials & Risk", fontsize=14)
plt.show()"""),
    md_cell("""### 2.3 Subjective Willingness vs Revealed True Risk (Behavioral Gap)"""),
    code_cell("""plt.figure(figsize=(9, 5))
risk_labels = {1: 'Substantial Risk', 2: 'Above Avg Risk', 3: 'Average Risk', 4: 'No Risk Willing'}
temp_df = df.copy()
temp_df['Risk_Label'] = temp_df['RISK07'].map(risk_labels)
sns.boxplot(data=temp_df, x='Risk_Label', y='TrueRiskTol', palette='magma')
plt.title("Subjective Survey Response vs Actual Revealed Risk Tolerance", fontsize=13)
plt.xlabel("Self-Reported Willingness (Questionnaire)")
plt.ylabel("Revealed True Risk Tolerance")
plt.ylim(0, 60)
plt.show()""")
]
create_notebook(cells_nb2, os.path.join(NOTEBOOKS_DIR, "02_Exploratory_Data_Analysis.ipynb"))

# =============================================================================
# Notebook 3: Regression Frameworks Benchmarking
# =============================================================================
cells_nb3 = [
    md_cell("""# 3. Model Training & 5-Framework Benchmarking
## Project: Modeling Investor Risk Tolerance & Enabling an ML-Based Robo-Advisor
**Course:** Machine Learning for Big Data (MLBD) — Mini Project, PES University  
**Authors:** Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), Chandraraj Patil (PES1UG24AM425)

---
### Frameworks Evaluated
1. **XGBoost**: Extreme Gradient Boosted Trees
2. **Keras**: Deep Multi-Layer Perceptron (PyTorch Backend)
3. **PyTorch with FastAI**: Tabular Learner with Embedding Layers & One-Cycle Policy
4. **PyTorch with TabNet**: Self-Attentive Tabular Architecture
5. **PyTorch Lightning**: Modular LightningModule Tabular Regressor

### Evaluation Criteria
- **Quantitative:** RMSE, MAE, R², MSE, Explained Variance, Training Time, Inference Latency
- **Qualitative:** Simplicity, Transparency, Efficacy"""),
    code_cell("""import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('..'))
from src.train_models import run_model_benchmarks

# Run the full benchmarking pipeline
benchmark_df = run_model_benchmarks()
benchmark_df"""),
    md_cell("""### 3.1 Inspect Quantitative Benchmark Comparison"""),
    code_cell("""cols = ['Framework', 'RMSE', 'MAE', 'R2', 'MSE', 'Train_Time_s', 'Latency_ms', 'Simplicity_Score (/10)', 'Transparency_Score (/10)', 'Efficacy_Score (/10)']
print(benchmark_df[cols].to_markdown(index=False))"""),
    md_cell("""### 3.2 Visual Comparison of Performance Metrics"""),
    code_cell("""fig, axes = plt.subplots(1, 3, figsize=(16, 4))
benchmark_df.plot(x='Framework', y='RMSE', kind='bar', ax=axes[0], color='#1f77b4', legend=False, rot=0)
axes[0].set_title("RMSE (Lower is Better)")

benchmark_df.plot(x='Framework', y='MAE', kind='bar', ax=axes[1], color='#ff7f0e', legend=False, rot=0)
axes[1].set_title("MAE (Lower is Better)")

benchmark_df.plot(x='Framework', y='R2', kind='bar', ax=axes[2], color='#2ca02c', legend=False, rot=0)
axes[2].set_title("R² Score (Higher is Better)")
plt.tight_layout()
plt.show()""")
]
create_notebook(cells_nb3, os.path.join(NOTEBOOKS_DIR, "03_Regression_Frameworks_Benchmarking.ipynb"))

# =============================================================================
# Notebook 4: Robo-Advisor Portfolio Optimization
# =============================================================================
cells_nb4 = [
    md_cell("""# 4. Robo-Advisor Portfolio Allocation Engine
## Project: Modeling Investor Risk Tolerance & Enabling an ML-Based Robo-Advisor
**Course:** Machine Learning for Big Data (MLBD) — Mini Project, PES University  
**Authors:** Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), Chandraraj Patil (PES1UG24AM425)

---
### Objectives
1. Implement Markowitz Modern Portfolio Theory (MPT) Mean-Variance Asset Allocation.
2. Dynamically link the investor's predicted Risk Tolerance to quadratic risk aversion $\\lambda$.
3. Optimize portfolio weights across selected S&P 500 assets.
4. Simulate historical backtest of a $100 investment."""),
    code_cell("""import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('..'))
from src.portfolio_optimization import load_market_data, get_asset_allocation

market_df = load_market_data('../data/SP500Data.csv')
print(f"Loaded market data with {market_df.shape[1]} assets.")"""),
    md_cell("""### 4.1 Mean-Variance Asset Allocation for Moderate Risk Investor (RT = 23.64)"""),
    code_cell("""selected_assets = ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT']
res_moderate = get_asset_allocation(risk_tolerance=23.64, selected_tickers=selected_assets, market_df=market_df)

print("Optimal Portfolio Weights:", res_moderate['weights'])
print(f"Expected Annual Return: {res_moderate['expected_annual_return']}%")
print(f"Annual Volatility: {res_moderate['annual_volatility']}%")
print(f"Sharpe Ratio: {res_moderate['sharpe_ratio']}")"""),
    md_cell("""### 4.2 Asset Allocation & $100 Investment Growth Plot (Figure 5-6 Style)"""),
    code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Asset allocation bar chart
axes[0].bar(list(res_moderate['weights'].keys()), list(res_moderate['weights'].values()), color='red', edgecolor='darkred')
axes[0].set_title("Asset Allocation - Mean-Variance Allocation")
axes[0].set_ylabel("Weight")
axes[0].set_ylim(0, 1.0)

# $100 Investment line chart
gdf = res_moderate['growth_df']
axes[1].plot(gdf.index, gdf['Portfolio_Value'], color='red', lw=2)
axes[1].set_title("Portfolio Value of $100 Investment")
axes[1].set_ylabel("Portfolio Value ($)")
axes[1].grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()""")
]
create_notebook(cells_nb4, os.path.join(NOTEBOOKS_DIR, "04_Robo_Advisor_Portfolio_Optimization.ipynb"))

