"""
Robo-Advisor Interactive Dashboard
Enables an end-to-end automated wealth management experience:
1. Predicts individual Investor Risk Tolerance using trained Supervised ML model
2. Dynamically calibrates Markowitz Mean-Variance Asset Allocation
3. Visualizes optimal asset weights and simulates $100 investment growth over time
Replicates Figure 5-6 from the assignment case study.
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Local imports
from src.portfolio_optimization import load_market_data, get_asset_allocation

# Streamlit Page Config
st.set_page_config(
    page_title="Robo Advisor Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark headers and card layout matching Figure 5-6
st.markdown("""
<style>
    .main-header {
        background-color: #111111;
        color: #ffffff;
        padding: 14px 20px;
        font-size: 24px;
        font-weight: bold;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .step-banner {
        background-color: #2b2b2b;
        color: #ffffff;
        padding: 10px 15px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }
    .calc-btn {
        background-color: #111111;
        color: white;
        font-weight: bold;
        border-radius: 4px;
        padding: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-header">Robo Advisor Dashboard</div>', unsafe_allow_html=True)

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
if "predicted_risk_tolerance" not in st.session_state:
    st.session_state["predicted_risk_tolerance"] = 23.64

# Two-column Layout matching Figure 5-6
col1, col2 = st.columns([1, 1.8], gap="large")

# =============================================================================
# COLUMN 1: STEP 1 - Enter Investor Characteristics
# =============================================================================
with col1:
    st.markdown('<div class="step-banner">Step 1 : Enter Investor Characteristics</div>', unsafe_allow_html=True)
    
    age = st.slider("Age:", min_value=20, max_value=85, value=45, step=1)
    networth = st.slider("NetWorth ($):", min_value=-500000, max_value=5000000, value=500000, step=25000, format="$%d")
    income = st.slider("Income ($):", min_value=10000, max_value=2000000, value=125000, step=10000, format="$%d")
    
    col_ed, col_mar = st.columns(2)
    with col_ed:
        edcl = st.slider("Education Level (scale 1-4):", min_value=1, max_value=4, value=3,
                         help="1: No HS, 2: High School, 3: Some College, 4: College Degree")
    with col_mar:
        married = st.slider("Married (1: Yes, 2: No):", min_value=1, max_value=2, value=1)
        
    col_kd, col_occ = st.columns(2)
    with col_kd:
        kids = st.slider("Kids:", min_value=0, max_value=7, value=2)
    with col_occ:
        occup = st.slider("Occupation (scale 1-4):", min_value=1, max_value=4, value=1,
                          help="1: Managerial/Prof, 2: Technical/Sales, 3: Production, 4: Unemployed/Retired")
                          
    risk_willingness = st.slider("Willingness to take Risk (scale 1-4):", min_value=1, max_value=4, value=2,
                                 help="1: Substantial Risk, 2: Above Average, 3: Average, 4: Not Willing")
    
    calc_button = st.button("CALCULATE RISK TOLERANCE", use_container_width=True)
    
    if calc_button:
        # Prepare input features vector: ['AGE07', 'EDCL07', 'MARRIED07', 'KIDS07', 'OCCAT107', 'INCOME07', 'RISK07', 'NETWORTH07']
        input_data = pd.DataFrame([{
            'AGE07': age,
            'EDCL07': edcl,
            'MARRIED07': married,
            'KIDS07': kids,
            'OCCAT107': occup,
            'INCOME07': income,
            'RISK07': risk_willingness,
            'NETWORTH07': networth
        }])
        
        pred_rt = float(model.predict(input_data)[0])
        pred_rt = np.clip(pred_rt, 0.5, 99.5)
        st.session_state["predicted_risk_tolerance"] = round(pred_rt, 2)
        st.success(f"Predicted True Risk Tolerance: **{st.session_state['predicted_risk_tolerance']} / 100**")

# =============================================================================
# COLUMN 2: STEP 2 - Asset Allocation and Portfolio Performance
# =============================================================================
with col2:
    st.markdown('<div class="step-banner">Step 2 : Asset Allocation and portfolio performance</div>', unsafe_allow_html=True)
    
    c_rt, c_sub = st.columns([1, 1])
    with c_rt:
        rt_input = st.number_input(
            "Risk Tolerance (scale of 100) :",
            min_value=0.1,
            max_value=100.0,
            value=float(st.session_state["predicted_risk_tolerance"]),
            step=0.5
        )
    
    # Available assets
    all_tickers = sorted(list(market_df.columns))
    default_tickers = [t for t in ['GOOGL', 'FB', 'GS', 'MS', 'GE', 'MSFT'] if t in all_tickers]
    
    selected_tickers = st.multiselect(
        "Select the assets for the portfolio:",
        options=all_tickers,
        default=default_tickers
    )
    
    submit_button = st.button("SUBMIT", use_container_width=False)
    
    if len(selected_tickers) < 2:
        st.warning("Please select at least 2 assets to optimize portfolio allocation.")
    else:
        # Run Markowitz Optimization
        alloc_res = get_asset_allocation(
            risk_tolerance=rt_input,
            selected_tickers=selected_tickers,
            market_df=market_df
        )
        
        # Display Key Financial Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Expected Annual Return", f"{alloc_res['expected_annual_return']}%")
        m2.metric("Annual Volatility (Risk)", f"{alloc_res['annual_volatility']}%")
        m3.metric("Sharpe Ratio", f"{alloc_res['sharpe_ratio']}")
        
        # Two side-by-side charts matching Figure 5-6
        ch1, ch2 = st.columns(2)
        
        with ch1:
            st.markdown("<h5 style='text-align: center; color: #111111;'>Asset allocation - Mean-Variance Allocation</h5>", unsafe_allow_html=True)
            fig_bar, ax_bar = plt.subplots(figsize=(6, 4.8))
            tickers = list(alloc_res['weights'].keys())
            weights = list(alloc_res['weights'].values())
            
            # Bright red bars matching Figure 5-6
            ax_bar.bar(tickers, weights, color='#ff0000', edgecolor='darkred', width=0.6)
            ax_bar.set_ylim(0, max(0.4, max(weights) * 1.25 if max(weights) > 0 else 0.4))
            ax_bar.set_ylabel("Portfolio Weight", fontsize=10)
            ax_bar.grid(axis='y', linestyle=':', alpha=0.6)
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
            ax_line.plot(gdf.index, gdf['Portfolio_Value'], color='#ff0000', linewidth=1.8)
            ax_line.set_ylabel("Portfolio Value ($)", fontsize=10)
            ax_line.grid(True, linestyle=':', alpha=0.6)
            
            # Format dates on x-axis
            x_ticks = np.linspace(0, len(gdf) - 1, 4, dtype=int)
            ax_line.set_xticks(gdf.index[x_ticks])
            ax_line.set_xticklabels([str(gdf.index[t])[:7] for t in x_ticks], fontsize=9)
            
            plt.tight_layout()
            st.pyplot(fig_line)
            plt.close()

# Footer Information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; font-size: 13px;'>
    <b>PES University — MLBD Mini Project</b><br>
    Team: Ananthakrishna M A (PES1UG24AM036) | Akash G K (PES1UG24AM022) | Amar Patil (PES1UG24AM031) | Chandraraj Patil (PES1UG24AM425)<br>
    Department of Computer Science and Engineering (AI & ML)
</div>
""", unsafe_allow_html=True)

