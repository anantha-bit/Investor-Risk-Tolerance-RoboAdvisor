"""
SCF Data Preprocessing Module
Extracts demographic, financial, and behavioral attributes from the Federal Reserve SCF 2009 panel data,
computes revealed risk tolerance before and after the 2008 financial crisis,
isolates intelligent investors with consistent risk profiles,
and prepares the normalized dataset for supervised regression modeling.
"""

import os
import numpy as np
import pandas as pd

SP500_AVG_2007 = 1478.0
SP500_AVG_2009 = 948.0

CORE_FEATURE_COLUMNS = [
    'AGE07',       # Age of individual
    'EDCL07',      # Education category (1: No HS, 2: HS, 3: Some college, 4: College degree)
    'MARRIED07',   # Marital status (1: Married, 2: Unmarried)
    'KIDS07',      # Number of kids
    'OCCAT107',    # Occupation category (1: Manager/Prof, 2: Tech/Sales/Service, 3: Production/Craft, 4: Unemployed/Retired)
    'INCOME07',    # Total household income
    'RISK07',      # Willingness to take risk (1: Take substantial risk, 2: Take above avg, 3: Take avg, 4: Not willing)
    'NETWORTH07'   # Net worth
]

TARGET_COLUMN = 'TrueRiskTol'

def preprocess_raw_scf_panel(raw_excel_path):
    """
    Reproduces the raw SCF feature extraction and target variable computation.
    """
    print(f"[PREPROCESS] Loading raw SCF panel dataset from {raw_excel_path}...")
    df = pd.read_excel(raw_excel_path)
    
    # 1. Risk-free assets: liquid accounts, CDs, savings bonds, cash life insurance
    df['RiskFree07'] = df['LIQ07'] + df['CDS07'] + df['SAVBND07'] + df['CASHLI07']
    df['RiskFree09'] = df['LIQ09'] + df['CDS09'] + df['SAVBND09'] + df['CASHLI09']
    
    # 2. Risky assets: mutual funds, stocks, bonds
    df['Risky07'] = df['NMMF07'] + df['STOCKS07'] + df['BOND07']
    df['Risky09'] = df['NMMF09'] + df['STOCKS09'] + df['BOND09']
    
    # Total liquid investment assets
    total_assets_07 = df['Risky07'] + df['RiskFree07']
    total_assets_09 = df['Risky09'] + df['RiskFree09']
    
    valid_mask = (total_assets_07 > 0) & (total_assets_09 > 0)
    df_valid = df[valid_mask].copy()
    
    # 3. Unadjusted Risk Tolerance
    df_valid['RT07'] = df_valid['Risky07'] / (df_valid['Risky07'] + df_valid['RiskFree07'])
    
    # 4. Normalized 2009 Risk Tolerance (adjusted by market drop from 1478 to 948)
    market_ratio = SP500_AVG_2009 / SP500_AVG_2007
    df_valid['RT09'] = (df_valid['Risky09'] / (df_valid['Risky09'] + df_valid['RiskFree09'])) * market_ratio
    
    # 5. Intelligent Investor Filter: investors whose risk tolerance changed by <= 10%
    df_valid['PercentageChange'] = np.abs(df_valid['RT09'] / df_valid['RT07'] - 1.0)
    df_clean = df_valid.dropna(subset=['RT07', 'RT09', 'PercentageChange'])
    df_clean = df_clean[~df_clean.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
    
    intelligent_investors = df_clean[df_clean['PercentageChange'] <= 0.10].copy()
    
    # 6. True Risk Tolerance (scaled to 0-100)
    intelligent_investors['TrueRiskTol'] = ((intelligent_investors['RT07'] + intelligent_investors['RT09']) / 2.0) * 100.0
    
    cols_to_keep = CORE_FEATURE_COLUMNS + [TARGET_COLUMN]
    final_df = intelligent_investors[cols_to_keep].dropna().reset_index(drop=True)
    return final_df

def load_clean_data(data_dir="data"):
    """
    Loads preprocessed dataset. If InputData.csv is available, loads and verifies it.
    Otherwise, processes SCFP2009panel.xlsx.
    """
    input_csv = os.path.join(data_dir, "InputData.csv")
    if os.path.exists(input_csv):
        print(f"[DATA] Loading processed dataset from {input_csv}...")
        df = pd.read_csv(input_csv, index_col=0)
        # Select key predictors and target
        features = [c for c in CORE_FEATURE_COLUMNS if c in df.columns]
        target = 'TrueRiskTol'
        return df[features + [target]].dropna().reset_index(drop=True)
    
    raw_excel = os.path.join(data_dir, "SCFP2009panel.xlsx")
    if os.path.exists(raw_excel):
        processed_df = preprocess_raw_scf_panel(raw_excel)
        processed_df.to_csv(input_csv)
        return processed_df
    
    raise FileNotFoundError("Neither InputData.csv nor SCFP2009panel.xlsx was found in data directory.")

if __name__ == "__main__":
    df = load_clean_data()
    print(f"Loaded dataset: {df.shape[0]} samples, {df.shape[1]} columns")
    print(df.head())
    print("\nTarget summary (TrueRiskTol):")
    print(df['TrueRiskTol'].describe())

