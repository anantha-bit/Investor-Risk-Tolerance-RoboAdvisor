"""
Markowitz Mean-Variance Portfolio Optimization Engine
Implements Modern Portfolio Theory (MPT) asset allocation dynamically calibrated
to the investor's dual-dimension Risk Tolerance and Financial Risk Capacity.

Key Features:
1. Two-Sleeve Architecture:
   - Defensive Sleeve (Cash / Fixed-Income / Treasury proxy at 2.5% yield, low volatility).
   - Equity Sleeve (Markowitz MPT optimal asset weights across user-selected equities).
2. Dynamic Risk Aversion (lambda) mapping:
   - Higher risk tolerance -> lower risk aversion -> higher equity risk premia.
   - Lower risk tolerance -> higher risk aversion -> prioritized capital preservation.
3. Capacity Gating:
   - Financially fragile investors (low capacity) are restricted by max_equity_allocation caps.
4. Comprehensive Metrics:
   - Expected Annual Return, Annual Volatility, Sharpe Ratio, and historical $100 backtest.
"""

import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize

DEFAULT_ASSETS = ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT']
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "SP500Data.csv")

RISK_FREE_RATE = 0.025 # 2.5% annualized risk-free cash/treasury yield
CASH_TICKER = "CASH/BONDS"

def load_market_data(csv_path=DATA_PATH):
    """
    Loads and cleans historical S&P 500 stock price data.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Market data file not found at {csv_path}")
    
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    
    # Remove columns with excessive missing data (>30%)
    missing_fraction = df.isnull().mean()
    drop_cols = missing_fraction[missing_fraction > 0.30].index.tolist()
    df = df.drop(columns=drop_cols)
    
    # Forward-fill remaining missing values
    df = df.ffill().bfill()
    return df


def get_asset_allocation(
    risk_tolerance: float,
    selected_tickers: list,
    market_df: pd.DataFrame = None,
    max_equity_cap: float = None,
    include_cash_sleeve: bool = True
):
    """
    Computes optimal asset allocation combining Modern Portfolio Theory (MPT) equity optimization
    with risk-category-governed defensive cash/bond allocation.
    
    Parameters:
    -----------
    risk_tolerance : float (0 to 100)
        Predicted or synthesized risk tolerance score
    selected_tickers : list of str
        Stock symbols selected for equity sleeve
    market_df : pd.DataFrame (optional)
        Historical price dataframe
    max_equity_cap : float (optional)
        Upper bound percentage for total equity allocation (governed by Financial Risk Capacity)
    include_cash_sleeve : bool
        Whether to include defensive cash/fixed-income sleeve (default True for real-world robo-advisors)
        
    Returns:
    --------
    dict containing:
        - weights: dict of ticker/asset -> total portfolio weight (sums to 1.0)
        - equity_sleeve_weights: dict of stock -> weight within equity sleeve
        - equity_allocation_pct: float
        - cash_allocation_pct: float
        - expected_annual_return: float (annualized %)
        - annual_volatility: float (annualized %)
        - sharpe_ratio: float
        - growth_df: pd.DataFrame of $100 historical backtest
    """
    if market_df is None:
        market_df = load_market_data()
        
    valid_tickers = [t for t in selected_tickers if t in market_df.columns]
    if len(valid_tickers) < 2:
        raise ValueError("Must select at least 2 valid asset tickers.")
        
    prices = market_df[valid_tickers].dropna()
    daily_returns = prices.pct_change().dropna()
    
    mean_daily_return = daily_returns.mean().values
    cov_daily = daily_returns.cov().values
    n_assets = len(valid_tickers)
    
    # 1. Calibrate Risk Aversion Parameter (lambda)
    # Correct Direction: Higher risk tolerance -> lower lambda (more weight on return)
    # Lower risk tolerance -> higher lambda (penalty on variance)
    rt_norm = float(np.clip(risk_tolerance, 1.0, 99.0))
    risk_aversion_lambda = (100.0 - rt_norm + 1.0) / 8.0 # Range: ~0.25 (aggressive) to ~12.5 (conservative)
    
    # 2. Markowitz Mean-Variance Optimization for Equity Sleeve
    # Objective: minimize (lambda/2 * w^T * Cov * w - w^T * mu)
    def objective(w):
        port_var = np.dot(w.T, np.dot(cov_daily, w))
        port_ret = np.dot(w, mean_daily_return)
        return (risk_aversion_lambda / 2.0) * port_var - port_ret
    
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    bounds = tuple((0.0, 1.0) for _ in range(n_assets))
    init_weights = np.ones(n_assets) / n_assets
    
    res = minimize(objective, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    if not res.success:
        eq_weights = init_weights
    else:
        eq_weights = res.x
        
    # Clean tiny near-zero values
    eq_weights = np.where(eq_weights < 0.005, 0.0, eq_weights)
    eq_weights = eq_weights / np.sum(eq_weights)
    
    # 3. Two-Sleeve Allocation (Cash/Bonds Defensive vs Equity Sleeve)
    if include_cash_sleeve:
        # Standard target equity percentage as function of Risk Tolerance:
        # RT 10 (Very Cons) -> 23% equity, 77% defensive
        # RT 30 (Cons)      -> 39% equity, 61% defensive
        # RT 50 (Mod)       -> 55% equity, 45% defensive
        # RT 70 (Mod Agg)   -> 71% equity, 29% defensive
        # RT 90 (Agg)       -> 87% equity, 13% defensive
        target_equity_pct = float(np.clip(15.0 + 0.80 * rt_norm, 15.0, 95.0))
        
        # Apply Financial Capacity constraint cap if provided
        if max_equity_cap is not None:
            target_equity_pct = min(target_equity_pct, float(max_equity_cap))
            
        equity_weight_total = target_equity_pct / 100.0
        cash_weight_total = 1.0 - equity_weight_total
    else:
        equity_weight_total = 1.0
        cash_weight_total = 0.0
        target_equity_pct = 100.0
        
    # Total portfolio weights
    total_weights = {}
    if cash_weight_total > 0.001:
        total_weights[CASH_TICKER] = round(cash_weight_total, 4)
    for tic, w in zip(valid_tickers, eq_weights):
        total_weights[tic] = round(float(w * equity_weight_total), 4)
        
    # Equity sleeve standalone metrics
    eq_ann_return = float(np.dot(eq_weights, mean_daily_return) * 252.0)
    eq_ann_volatility = float(np.sqrt(np.dot(eq_weights.T, np.dot(cov_daily * 252.0, eq_weights))))
    
    # Total portfolio metrics
    # Daily cash return proxy
    daily_rf = RISK_FREE_RATE / 252.0
    total_ann_return = float(cash_weight_total * RISK_FREE_RATE + equity_weight_total * eq_ann_return)
    total_ann_volatility = float(equity_weight_total * eq_ann_volatility) # Cash has ~0 correlation and minimal volatility
    
    sharpe_ratio = float((total_ann_return - RISK_FREE_RATE) / total_ann_volatility) if total_ann_volatility > 0.001 else 0.0
    
    # 4. Historical Portfolio $100 Backtest Growth Trajectory
    port_eq_daily_ret = (daily_returns * eq_weights).sum(axis=1)
    port_total_daily_ret = cash_weight_total * daily_rf + equity_weight_total * port_eq_daily_ret
    cum_growth = 100.0 * (1.0 + port_total_daily_ret).cumprod()
    
    growth_df = pd.DataFrame({
        'Date': prices.index[1:],
        'Portfolio_Value': cum_growth.values
    }).set_index('Date')
    
    eq_sleeve_weights_dict = {tic: round(float(w), 4) for tic, w in zip(valid_tickers, eq_weights)}
    
    return {
        'tickers': valid_tickers,
        'weights': total_weights,
        'equity_sleeve_weights': eq_sleeve_weights_dict,
        'equity_allocation_pct': round(target_equity_pct, 1),
        'cash_allocation_pct': round(cash_weight_total * 100.0, 1),
        'risk_aversion_lambda': round(risk_aversion_lambda, 3),
        'expected_annual_return': round(total_ann_return * 100.0, 2),
        'annual_volatility': round(total_ann_volatility * 100.0, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'growth_df': growth_df
    }


if __name__ == "__main__":
    market = load_market_data()
    print("Testing MPT Asset Allocation across standard Risk Categories:")
    for rt, name in [(10, "Very Conservative"), (30, "Conservative"), (50, "Moderate"), (70, "Mod Aggressive"), (90, "Aggressive")]:
        alloc = get_asset_allocation(rt, ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT'], market)
        print(f"  RT={rt:2d} ({name:18s}): Cash={alloc['cash_allocation_pct']}% | Eq={alloc['equity_allocation_pct']}% | Return={alloc['expected_annual_return']}% | Vol={alloc['annual_volatility']}% | Sharpe={alloc['sharpe_ratio']}")
