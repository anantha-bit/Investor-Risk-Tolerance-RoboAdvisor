"""
Robo-Advisor Interactive Dashboard
Enables an end-to-end automated wealth management experience:
1. Predicts dual-dimension Investor Risk:
   - Financial Risk Capacity (Objective balance sheet ability to absorb losses)
   - Psychological Risk Willingness (Subjective risk tolerance & loss aversion)
2. Synthesizes a calibrated Final Risk Assessment with fiduciary capacity gating.
3. Provides granular explainability in "Why Did We Assign This Risk Profile?".
4. Dynamically calibrates Markowitz Mean-Variance Asset Allocation with defensive cash/bond sleeve.
5. Visualizes optimal asset weights and simulates $100 investment growth over time.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Local imports
from src.portfolio_optimization import load_market_data, get_asset_allocation, CASH_TICKER
from src.risk_assessment import (
    evaluate_final_risk_profile,
    get_risk_tier,
    RISK_CATEGORIES
)

# Streamlit Page Config
st.set_page_config(
    page_title="Robo Advisor Dashboard | Dual-Dimension Risk Profiler",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern card layout and dark headers matching Figure 5-6
st.markdown("""
<style>
    .main-header {
        background-color: #111111;
        color: #ffffff;
        padding: 16px 22px;
        font-size: 26px;
        font-weight: 700;
        border-radius: 6px;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    .step-banner {
        background-color: #2b2b2b;
        color: #ffffff;
        padding: 10px 16px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-card {
        display: inline-block;
        padding: 6px 14px;
        font-size: 15px;
        font-weight: bold;
        color: white;
        border-radius: 20px;
        margin-top: 5px;
    }
    .factor-box-support {
        background-color: #eafaf1;
        border-left: 4px solid #2ecc71;
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 13.5px;
        color: #196f3d;
    }
    .factor-box-caution {
        background-color: #fef9e7;
        border-left: 4px solid #f39c12;
        padding: 10px 14px;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 13.5px;
        color: #9a7d0a;
    }
    .fiduciary-box {
        background-color: #ebf5fb;
        border-left: 4px solid #2980b9;
        padding: 10px 14px;
        border-radius: 4px;
        margin-top: 10px;
        font-size: 13px;
        color: #1b4f72;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-header">Robo Advisor Dashboard — ML Risk Tolerance & Portfolio Allocation</div>', unsafe_allow_html=True)

# Load Model and Market Data
@st.cache_resource
def load_resources():
    model_path = os.path.join(os.path.dirname(__file__), "models", "finalized_model.sav")
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "models", "best_model.joblib")
    model = joblib.load(model_path)
    market_df = load_market_data()
    return model, market_df

try:
    model, market_df = load_resources()
except Exception as e:
    st.error(f"Error loading model or market data: {e}")
    st.stop()

# Initialize Session State
if "profile_result" not in st.session_state:
    # Default baseline profile
    st.session_state["profile_result"] = evaluate_final_risk_profile(
        income=125000,
        networth=500000,
        liquid_savings=60000,
        debt=25000,
        kids=2,
        age=45,
        education=3,
        marital_status=1,
        occupation=1,
        risk_willingness_scale=2,
        downturn_reaction=2,
        investment_horizon=15,
        currency="USD"
    )

prof = st.session_state["profile_result"]

# Two-column Layout matching Figure 5-6
col1, col2 = st.columns([1.1, 1.7], gap="large")

# =============================================================================
# COLUMN 1: STEP 1 - Enter Investor Characteristics & Dual Risk Profile
# =============================================================================
with col1:
    st.markdown('<div class="step-banner">Step 1 : Enter Investor Characteristics</div>', unsafe_allow_html=True)
    
    # Currency toggle
    c_curr, c_space = st.columns([1, 1])
    with c_curr:
        currency = st.radio("Select Currency:", options=["USD ($)", "INR (₹)"], horizontal=True)
    is_inr = "INR" in currency
    curr_sym = "₹" if is_inr else "$"
    
    # Financial Inputs
    c_age, c_horiz = st.columns(2)
    with c_age:
        age = st.slider("Age:", min_value=18, max_value=85, value=45, step=1)
    with c_horiz:
        horizon = st.slider("Investment Horizon (years):", min_value=1, max_value=35, value=15, step=1,
                            help="Expected duration before capital withdrawals begin.")
        
    if is_inr:
        income = st.slider("Annual Income (₹):", min_value=0, max_value=10000000, value=1200000, step=50000,
                           format="₹%d", help="Gross annual household income.")
        networth = st.slider("Net Worth (₹):", min_value=-1000000, max_value=50000000, value=5000000, step=100000,
                             format="₹%d", help="Total assets minus all outstanding debt.")
        liquid_savings = st.slider("Liquid Emergency Savings (₹):", min_value=0, max_value=10000000, value=500000, step=50000,
                                   format="₹%d", help="Bank savings, fixed deposits, liquid mutual funds.")
        debt = st.slider("Outstanding Debt (₹):", min_value=0, max_value=10000000, value=300000, step=50000,
                         format="₹%d", help="Mortgages, personal loans, car loans, credit cards.")
    else:
        income = st.slider("Annual Income ($):", min_value=0, max_value=2000000, value=125000, step=10000,
                           format="$%d", help="Gross annual household income.")
        networth = st.slider("Net Worth ($):", min_value=-200000, max_value=5000000, value=500000, step=25000,
                             format="$%d", help="Total assets minus all outstanding liabilities.")
        liquid_savings = st.slider("Liquid Emergency Savings ($):", min_value=0, max_value=1000000, value=60000, step=5000,
                                   format="$%d", help="Readily accessible bank cash & money-market funds.")
        debt = st.slider("Outstanding Debt ($):", min_value=0, max_value=1000000, value=35000, step=5000,
                         format="$%d", help="Total outstanding debt / loans.")

    # Demographic & Behavioral Inputs
    col_ed, col_mar = st.columns(2)
    with col_ed:
        edcl = st.selectbox(
            "Education Level:",
            options=[1, 2, 3, 4],
            index=2,
            format_func=lambda x: {1: "1: No High School", 2: "2: High School", 3: "3: Some College", 4: "4: College Degree"}[x]
        )
    with col_mar:
        married = st.selectbox(
            "Marital Status:",
            options=[1, 2],
            index=0,
            format_func=lambda x: {1: "1: Married", 2: "2: Unmarried / Single"}[x]
        )
        
    col_kd, col_occ = st.columns(2)
    with col_kd:
        kids = st.slider("Financial Dependents (Kids):", min_value=0, max_value=7, value=2)
    with col_occ:
        occup = st.selectbox(
            "Occupation Stability:",
            options=[1, 2, 3, 4],
            index=0,
            format_func=lambda x: {1: "1: Managerial / Prof.", 2: "2: Technical / Sales", 3: "3: Production / Craft", 4: "4: Unemployed / Retired"}[x]
        )
        
    risk_willingness = st.select_slider(
        "Psychological Risk Willingness:",
        options=[1, 2, 3, 4],
        value=2,
        format_func=lambda x: {
            1: "1: Take Substantial Risk (High Returns)",
            2: "2: Take Above Average Risk",
            3: "3: Take Average Risk",
            4: "4: Not Willing to Take Any Risk"
        }[x],
        help="Self-reported psychological comfort with investment volatility."
    )
    
    downturn_react = st.selectbox(
        "Reaction to a 20% Market Downturn:",
        options=[1, 2, 3, 4],
        index=1,
        format_func=lambda x: {
            1: "1: Buy Aggressively on the Dip",
            2: "2: Hold Steady & Rebalance",
            3: "3: Feel Anxious & Reduce Equity Exposure",
            4: "4: Panic & Liquidate to 100% Cash"
        }[x]
    )
    
    calc_button = st.button("CALCULATE DUAL-DIMENSION RISK PROFILE", use_container_width=True)
    
    if calc_button:
        # Currency identifier
        curr_code = "INR" if is_inr else "USD"
        
        # Evaluate Dual-Dimension Profile
        prof = evaluate_final_risk_profile(
            income=income,
            networth=networth,
            liquid_savings=liquid_savings,
            debt=debt,
            kids=kids,
            age=age,
            education=edcl,
            marital_status=married,
            occupation=occup,
            risk_willingness_scale=risk_willingness,
            downturn_reaction=downturn_react,
            investment_horizon=horizon,
            currency=curr_code
        )
        st.session_state["profile_result"] = prof
        st.success(f"Risk Assessment Complete: **{prof['risk_category']}** ({prof['final_risk_score']:.1f} / 100)")

    # -------------------------------------------------------------------------
    # Risk Assessment Results & Explainability
    # -------------------------------------------------------------------------
    prof = st.session_state["profile_result"]
    
    st.markdown("---")
    st.markdown("#### Dual-Dimension Assessment Scores")
    
    # 4 Key Metric Cards
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:13px; color:#555;">Financial Risk Capacity</span>
            <div style="font-size:24px; font-weight:bold; color:#1f77b4;">{prof['financial_capacity_score']:.1f} <span style="font-size:14px;">/ 100</span></div>
            <span style="font-size:12px; color:#777;">Objective Loss Absorption Ability</span>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <span style="font-size:13px; color:#555;">Psychological Risk Willingness</span>
            <div style="font-size:24px; font-weight:bold; color:#ff7f0e;">{prof['psychological_willingness_score']:.1f} <span style="font-size:14px;">/ 100</span></div>
            <span style="font-size:12px; color:#777;">Subjective Risk Tolerance</span>
        </div>
        """, unsafe_allow_html=True)
        
    m3, m4 = st.columns(2)
    with m3:
        st.markdown(f"""
        <div class="metric-card" style="margin-top:10px;">
            <span style="font-size:13px; color:#555;">Final Investor Category</span>
            <div style="margin-top:4px;"><span class="badge-card" style="background-color:{prof['badge_color']};">{prof['risk_category']}</span></div>
            <div style="font-size:12px; color:#777; margin-top:5px;">Composite Score: <b>{prof['final_risk_score']:.1f} / 100</b></div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card" style="margin-top:10px;">
            <span style="font-size:13px; color:#555;">Financial Stability Score</span>
            <div style="font-size:24px; font-weight:bold; color:#2ca02c;">{prof['financial_stability_score']:.1f} <span style="font-size:14px;">/ 100</span></div>
            <span style="font-size:12px; color:#777;">Solvency & Emergency Cushion</span>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # Section: "Why Did We Assign This Risk Profile?"
    # -------------------------------------------------------------------------
    st.markdown("<h5 style='margin-top:20px; color:#111111;'>Why Did We Assign This Risk Profile?</h5>", unsafe_allow_html=True)
    
    st.markdown("<b>Factors supporting higher risk capacity:</b>", unsafe_allow_html=True)
    if prof["supporting_factors"]:
        for factor in prof["supporting_factors"]:
            st.markdown(f"<div class='factor-box-support'>✔ {factor}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='factor-box-support'>No high-capacity financial tailwinds detected.</div>", unsafe_allow_html=True)
        
    st.markdown("<b>Factors suggesting caution & constraints:</b>", unsafe_allow_html=True)
    if prof["caution_factors"]:
        for factor in prof["caution_factors"]:
            st.markdown(f"<div class='factor-box-caution'>⚠ {factor}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='factor-box-caution'>No significant balance sheet vulnerabilities detected.</div>", unsafe_allow_html=True)
        
    # Distinction between Model Prediction & Rule-based Constraints
    if prof.get("constraint_applied"):
        st.markdown(f"""
        <div class='fiduciary-box'>
            <b>🛡 Fiduciary Safety Constraint Triggered:</b><br>
            {prof['constraint_applied']}<br>
            <i>Rule-based financial capacity constraints supersede machine learning predictions to ensure capital preservation.</i>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='fiduciary-box'>
            <b>✔ Unconstrained Synthesis:</b><br>
            Financial Risk Capacity (35%) and Psychological Risk Willingness (65%) are mutually consistent. No overriding fiduciary constraint was required.
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# COLUMN 2: STEP 2 - Asset Allocation and Portfolio Performance (Markowitz MPT)
# =============================================================================
with col2:
    st.markdown('<div class="step-banner">Step 2 : Asset Allocation and portfolio performance</div>', unsafe_allow_html=True)
    
    prof = st.session_state["profile_result"]
    
    c_rt, c_cat = st.columns([1, 1.2])
    with c_rt:
        rt_input = st.number_input(
            "Calibrated Risk Tolerance (scale 0-100):",
            min_value=0.1,
            max_value=100.0,
            value=float(prof["final_risk_score"]),
            step=0.5
        )
    with c_cat:
        st.markdown(f"<div style='margin-top:28px;'>Category: <b>{get_risk_tier(rt_input)}</b> | Max Equity Cap: <b>{prof['max_equity_allocation']:.0f}%</b></div>", unsafe_allow_html=True)
    
    # Available assets
    all_tickers = sorted(list(market_df.columns))
    default_tickers = [t for t in ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT'] if t in all_tickers]
    
    selected_tickers = st.multiselect(
        "Select the assets for the equity sleeve:",
        options=all_tickers,
        default=default_tickers
    )
    
    submit_button = st.button("OPTIMIZE PORTFOLIO ALLOCATION", use_container_width=False)
    
    if len(selected_tickers) < 2:
        st.warning("Please select at least 2 equity assets to optimize mean-variance allocation.")
    else:
        # Run Markowitz Optimization with defensive cash/bond sleeve
        alloc_res = get_asset_allocation(
            risk_tolerance=rt_input,
            selected_tickers=selected_tickers,
            market_df=market_df,
            max_equity_cap=prof["max_equity_allocation"],
            include_cash_sleeve=True
        )
        
        # Display Key Financial Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Expected Annual Return", f"{alloc_res['expected_annual_return']}%")
        m2.metric("Annual Volatility (Risk)", f"{alloc_res['annual_volatility']}%")
        m3.metric("Sharpe Ratio", f"{alloc_res['sharpe_ratio']}")
        m4.metric("Cash vs Equity Split", f"{alloc_res['cash_allocation_pct']:.0f}% / {alloc_res['equity_allocation_pct']:.0f}%")
        
        # Two side-by-side charts matching Figure 5-6
        ch1, ch2 = st.columns(2)
        
        with ch1:
            st.markdown("<h5 style='text-align: center; color: #111111;'>Asset allocation - Mean-Variance Allocation</h5>", unsafe_allow_html=True)
            fig_bar, ax_bar = plt.subplots(figsize=(6, 4.8))
            
            tickers = list(alloc_res['weights'].keys())
            weights = list(alloc_res['weights'].values())
            
            # Highlight CASH/BONDS in blue, Equities in red
            bar_colors = ['#2980b9' if t == CASH_TICKER else '#ff0000' for t in tickers]
            edge_colors = ['#1b4f72' if t == CASH_TICKER else 'darkred' for t in tickers]
            
            ax_bar.bar(tickers, weights, color=bar_colors, edgecolor=edge_colors, width=0.6)
            ax_bar.set_ylim(0, max(0.4, max(weights) * 1.25 if max(weights) > 0 else 0.4))
            ax_bar.set_ylabel("Portfolio Weight", fontsize=10)
            ax_bar.grid(axis='y', linestyle=':', alpha=0.6)
            ax_bar.tick_params(axis='x', rotation=20)
            for i, w in enumerate(weights):
                if w > 0.01:
                    ax_bar.text(i, w + 0.01, f"{w:.2f}", ha='center', fontsize=9, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig_bar)
            plt.close()
            
        with ch2:
            st.markdown("<h5 style='text-align: center; color: #111111;'>Portfolio value of $100 investment</h5>", unsafe_allow_html=True)
            fig_line, ax_line = plt.subplots(figsize=(6, 4.8))
            gdf = alloc_res['growth_df']
            
            # Red line matching Figure 5-6
            ax_line.plot(gdf.index, gdf['Portfolio_Value'], color='#ff0000', linewidth=1.8, label="Simulated Backtest")
            ax_line.set_ylabel("Portfolio Value ($)", fontsize=10)
            ax_line.grid(True, linestyle=':', alpha=0.6)
            
            # Format dates on x-axis
            x_ticks = np.linspace(0, len(gdf) - 1, 4, dtype=int)
            ax_line.set_xticks(gdf.index[x_ticks])
            ax_line.set_xticklabels([str(gdf.index[t])[:7] for t in x_ticks], fontsize=9)
            
            plt.tight_layout()
            st.pyplot(fig_line)
            plt.close()
            
        # Summary description
        st.markdown(f"""
        <div style='background-color:#f8f9fa; border:1px solid #dee2e6; border-radius:4px; padding:12px; margin-top:10px; font-size:13px;'>
            <b>Portfolio Summary for {prof['risk_category']} Investor:</b><br>
            • <b>Defensive Sleeve:</b> {alloc_res['cash_allocation_pct']:.1f}% allocated to {CASH_TICKER} (yield 2.5%, near-zero volatility) to enforce capacity constraints.<br>
            • <b>Equity Sleeve:</b> {alloc_res['equity_allocation_pct']:.1f}% optimized via Markowitz MPT (risk aversion parameter &lambda; = {alloc_res['risk_aversion_lambda']:.2f}).<br>
            • <b>Risk-Adjusted Performance:</b> Portfolio achieves an annualized return of <b>{alloc_res['expected_annual_return']}%</b> with an annual volatility of <b>{alloc_res['annual_volatility']}%</b> (Sharpe ratio: <b>{alloc_res['sharpe_ratio']}</b>).
        </div>
        """, unsafe_allow_html=True)

# Footer Information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 13px;'>
    <b>PES University — MLBD Mini Project</b><br>
    Team: Ananthakrishna M A (PES1UG24AM036) | Akash G K (PES1UG24AM022) | Amar Patil (PES1UG24AM031) | Chandraraj Patil (PES1UG24AM425)<br>
    Department of Computer Science and Engineering (AI & ML)
</div>
""", unsafe_allow_html=True)
