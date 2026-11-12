"""
Markowitz Mean-Variance Portfolio Optimization Engine
Implements Modern Portfolio Theory (MPT) asset allocation dynamically calibrated
to the individual investor's predicted Risk Tolerance score.
Computes optimal asset weights, expected annual return, volatility, Sharpe ratio,
and simulates historical backtest growth of a $100 investment.
"""

import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize

DEFAULT_ASSETS = ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT']
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "SP500Data.csv")

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

def get_asset_allocation(risk_tolerance, selected_tickers, market_df=None):
    """
    Computes optimal asset weights using Markowitz Mean-Variance Optimization.
    
    Parameters:
    -----------
    risk_tolerance : float (0 to 100)
        Predicted risk tolerance of investor
    selected_tickers : list of str
        Stock symbols selected for portfolio
    market_df : pd.DataFrame (optional)
        Historical price dataframe
        
    Returns:
    --------
    dict containing:
        - weights: dict of ticker -> weight
        - expected_annual_return: float
        - annual_volatility: float
        - sharpe_ratio: float
        - cumulative_growth_df: pd.DataFrame of $100 investment
    """
    if market_df is None:
        market_df = load_market_data()
        
    # Filter available tickers
    valid_tickers = [t for t in selected_tickers if t in market_df.columns]
    if len(valid_tickers) < 2:
        raise ValueError("Must select at least 2 valid asset tickers.")
        
    prices = market_df[valid_tickers].dropna()
    daily_returns = prices.pct_change().dropna()
    
    mean_daily_return = daily_returns.mean().values
    cov_daily = daily_returns.cov().values
    n_assets = len(valid_tickers)
    
    # Calibrate risk aversion parameter lambda from risk tolerance (0-100)
    # Higher risk tolerance -> lower lambda (more weight on returns, higher equity risk)
    # Lower risk tolerance -> higher lambda (more penalty on variance, balanced/defensive)
    # Range of lambda: ~ 0.5 (aggressive, RT=100) to 12.0 (conservative, RT=0)
    rt_norm = np.clip(float(risk_tolerance), 0.1, 100.0)
    risk_aversion_lambda = (100.0 - rt_norm + 1.0) / 8.5
    
    # Objective function: minimize (lambda/2 * w^T * Cov * w - w^T * mu)
    def objective(w):
        port_var = np.dot(w.T, np.dot(cov_daily, w))
        port_ret = np.dot(w, mean_daily_return)
        return (risk_aversion_lambda / 2.0) * port_var - port_ret
    
    # Constraints: sum(w) = 1, bounds: 0 <= w_i <= 1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
    bounds = tuple((0.0, 1.0) for _ in range(n_assets))
    init_weights = np.ones(n_assets) / n_assets
    
    res = minimize(objective, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    if not res.success:
        optimal_weights = init_weights
    else:
        optimal_weights = res.x
        
    # Clean tiny near-zero values
    optimal_weights = np.where(optimal_weights < 0.001, 0.0, optimal_weights)
    optimal_weights = optimal_weights / np.sum(optimal_weights)
    
    # Performance metrics (Annualized: 252 trading days)
    ann_return = float(np.dot(optimal_weights, mean_daily_return) * 252.0)
    ann_volatility = float(np.sqrt(np.dot(optimal_weights.T, np.dot(cov_daily * 252.0, optimal_weights))))
    risk_free_rate = 0.02
    sharpe_ratio = float((ann_return - risk_free_rate) / ann_volatility) if ann_volatility > 0 else 0.0
    
    # Historical portfolio $100 backtest growth trajectory
    port_daily_ret = (daily_returns * optimal_weights).sum(axis=1)
    cum_growth = 100.0 * (1.0 + port_daily_ret).cumprod()
    
    growth_df = pd.DataFrame({
        'Date': prices.index[1:],
        'Portfolio_Value': cum_growth.values
    }).set_index('Date')
    
    weights_dict = {tic: round(float(w), 4) for tic, w in zip(valid_tickers, optimal_weights)}
    
    return {
        'tickers': valid_tickers,
        'weights': weights_dict,
        'expected_annual_return': round(ann_return * 100.0, 2),
        'annual_volatility': round(ann_volatility * 100.0, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'growth_df': growth_df
    }

if __name__ == "__main__":
    market = load_market_data()
    print(f"Loaded market data with {market.shape[1]} assets and {market.shape[0]} dates.")
    res = get_asset_allocation(risk_tolerance=23.64, selected_tickers=['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT'], market_df=market)
    print("Optimal Weights (RT=23.64):", res['weights'])
    print(f"Expected Return: {res['expected_annual_return']}% | Volatility: {res['annual_volatility']}% | Sharpe: {res['sharpe_ratio']}")
    print(res['growth_df'].tail())

