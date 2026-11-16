"""
SCF Data Preprocessing Module
Extracts demographic, financial, and behavioral attributes from the Federal Reserve SCF 2009 panel data,
computes:
1. Revealed Risk Tolerance (historical 2007-2009 asset allocation ratio)
2. Objective Financial Risk Capacity (loss absorption ability)
3. Subjective Psychological Risk Willingness (loss aversion / risk preference)
4. Synthesized Final Risk Tolerance & Category (calibrated with fiduciary gating)

Prepares the clean, enriched dataset for supervised regression and classification benchmarking.
"""

import os
import sys
import numpy as np
import pandas as pd

# Support both module and script execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try:
    from src.risk_assessment import evaluate_final_risk_profile
except ImportError:
    from risk_assessment import evaluate_final_risk_profile

SP500_AVG_2007 = 1478.0
SP500_AVG_2009 = 948.0

CORE_FEATURE_COLUMNS = [
    'AGE07',       # Age of individual
    'EDCL07',      # Education category (1: No HS, 2: HS, 3: Some college, 4: College degree)
    'MARRIED07',   # Marital status (1: Married, 2: Unmarried)
    'KIDS07',      # Number of kids / dependents
    'OCCAT107',    # Occupation category (1: Manager/Prof, 2: Tech/Sales/Service, 3: Production/Craft, 4: Unemployed/Retired)
    'INCOME07',    # Total household annual income
    'RISK07',      # Willingness to take risk (1: Take substantial risk, 2: Take above avg, 3: Take avg, 4: Not willing)
    'NETWORTH07'   # Net worth
]

DERIVED_COLUMNS = [
    'FinancialRiskCapacity',
    'PsychologicalRiskWillingness',
    'FinalRiskTolerance',
    'RiskCategory',
    'RevealedRiskTolerance'
]

TARGET_COLUMN = 'FinalRiskTolerance'
LEGACY_TARGET_COLUMN = 'TrueRiskTol'


def enrich_scf_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Financial Risk Capacity, Psychological Risk Willingness, Final Risk Tolerance,
    and 5-tier Risk Category for every observation in the dataframe.
    """
    df = df.copy()
    
    cap_scores = []
    will_scores = []
    final_scores = []
    categories = []
    
    for _, row in df.iterrows():
        age = int(row['AGE07'])
        horizon = max(1, 65 - age) if age < 65 else 5
        wsaved = int(row.get('WSAVED07', 2))
        
        prof = evaluate_final_risk_profile(
            income=float(row['INCOME07']),
            networth=float(row['NETWORTH07']),
            liquid_savings=float(row.get('LIQ07', 0.0)) if 'LIQ07' in df.columns else None,
            debt=float(row.get('DEBT07', 0.0)) if 'DEBT07' in df.columns else None,
            kids=int(row['KIDS07']),
            age=age,
            education=int(row['EDCL07']),
            marital_status=int(row['MARRIED07']),
            occupation=int(row['OCCAT107']),
            risk_willingness_scale=int(row['RISK07']),
            downturn_reaction=2,
            investment_horizon=horizon,
            wsaved=wsaved,
            currency="USD"
        )
        cap_scores.append(prof["financial_capacity_score"])
        will_scores.append(prof["psychological_willingness_score"])
        final_scores.append(prof["final_risk_score"])
        categories.append(prof["risk_category"])
        
    df['FinancialRiskCapacity'] = cap_scores
    df['PsychologicalRiskWillingness'] = will_scores
    df['FinalRiskTolerance'] = final_scores
    df['RiskCategory'] = categories
    
    # Store legacy revealed tolerance
    if 'RevealedRiskTolerance' not in df.columns:
        if 'TrueRiskTol' in df.columns:
            df['RevealedRiskTolerance'] = df['TrueRiskTol']
        else:
            df['RevealedRiskTolerance'] = df['FinalRiskTolerance']
            
    df['TrueRiskTol'] = df['FinalRiskTolerance']
    return df


def preprocess_raw_scf_panel(raw_excel_path):
    """
    Processes raw SCF panel dataset, extracts core predictors and financial features,
    and computes dual-dimension targets and revealed risk tolerance.
    """
    print(f"[PREPROCESS] Loading raw SCF panel dataset from {raw_excel_path}...")
    needed_cols = [
        'YY1', 'Y1', 'AGE07', 'EDCL07', 'MARRIED07', 'KIDS07', 'LIFECL07', 'OCCAT107',
        'INCOME07', 'RISK07', 'WSAVED07', 'SPENDMOR07', 'NETWORTH07', 'ASSET07', 'DEBT07',
        'LIQ07', 'CDS07', 'SAVBND07', 'CASHLI07', 'NMMF07', 'STOCKS07', 'BOND07',
        'LIQ09', 'CDS09', 'SAVBND09', 'CASHLI09', 'NMMF09', 'STOCKS09', 'BOND09'
    ]
    df = pd.read_excel(raw_excel_path, usecols=lambda c: c in needed_cols)
    
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
    
    # 4. Normalized 2009 Risk Tolerance
    market_ratio = SP500_AVG_2009 / SP500_AVG_2007
    df_valid['RT09'] = (df_valid['Risky09'] / (df_valid['Risky09'] + df_valid['RiskFree09'])) * market_ratio
    
    # 5. Intelligent Investor Filter (<= 10% change)
    df_valid['PercentageChange'] = np.abs(df_valid['RT09'] / df_valid['RT07'] - 1.0)
    df_clean = df_valid.dropna(subset=['RT07', 'RT09', 'PercentageChange'])
    df_clean = df_clean[~df_clean.isin([np.nan, np.inf, -np.inf]).any(axis=1)]
    
    intelligent_investors = df_clean[df_clean['PercentageChange'] <= 0.10].copy()
    intelligent_investors['RevealedRiskTolerance'] = ((intelligent_investors['RT07'] + intelligent_investors['RT09']) / 2.0) * 100.0
    
    # 6. Enrich with dual dimensions
    enriched_df = enrich_scf_dataframe(intelligent_investors)
    return enriched_df.reset_index(drop=True)


def load_clean_data(data_dir="data", target_col="FinalRiskTolerance"):
    """
    Loads preprocessed and enriched dataset.
    If InputData.csv is available, verifies and ensures dual-dimension columns are present.
    """
    input_csv = os.path.join(data_dir, "InputData.csv")
    if os.path.exists(input_csv):
        df = pd.read_csv(input_csv, index_col=0)
        # Check if already enriched
        if "FinancialRiskCapacity" not in df.columns or "FinalRiskTolerance" not in df.columns:
            print(f"[DATA] Enriching {input_csv} with dual-dimension risk targets...")
            df = enrich_scf_dataframe(df)
            df.to_csv(input_csv)
            print(f"[DATA] Saved enriched dataset to {input_csv}.")
            
        features = [c for c in CORE_FEATURE_COLUMNS if c in df.columns]
        target = target_col if target_col in df.columns else "FinalRiskTolerance"
        return df
        
    raw_excel = os.path.join(data_dir, "SCFP2009panel.xlsx")
    if os.path.exists(raw_excel):
        processed_df = preprocess_raw_scf_panel(raw_excel)
        processed_df.to_csv(input_csv)
        return processed_df
        
    raise FileNotFoundError("Neither InputData.csv nor SCFP2009panel.xlsx was found in data directory.")


if __name__ == "__main__":
    df = load_clean_data()
    print(f"Loaded dataset: {df.shape[0]} samples, {df.shape[1]} columns")
    print(df[CORE_FEATURE_COLUMNS + DERIVED_COLUMNS].head())
    print("\nFinal Risk Tolerance summary:")
    print(df['FinalRiskTolerance'].describe())
    print("\nRisk Category Distribution:")
    print(df['RiskCategory'].value_counts())
