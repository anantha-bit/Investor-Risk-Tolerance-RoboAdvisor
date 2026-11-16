"""
Risk Assessment Engine: Dual-Dimension Risk Profiling Framework
Separates Financial Risk Capacity (Objective Ability) and Psychological Risk Willingness (Subjective Tolerance),
applies asymmetric fiduciary gating (capacity ceiling and willingness governor),
and provides transparent factor explainability for the Robo-Advisor.
"""

import numpy as np
import pandas as pd

# Risk Category Definitions and Allocations
RISK_CATEGORIES = {
    "Very Conservative": {
        "range": (0.0, 20.0),
        "description": "Primary goal is capital preservation with minimal volatility.",
        "max_equity_pct": 20.0,
        "recommended_cash_bond_pct": 80.0,
        "badge_color": "#2b5c8f"
    },
    "Conservative": {
        "range": (20.0, 40.0),
        "description": "Defensive growth with income; accepts low-to-moderate short-term drawdowns.",
        "max_equity_pct": 35.0,
        "recommended_cash_bond_pct": 65.0,
        "badge_color": "#1f77b4"
    },
    "Moderate": {
        "range": (40.0, 60.0),
        "description": "Balanced growth and capital preservation; accepts normal market cycles.",
        "max_equity_pct": 55.0,
        "recommended_cash_bond_pct": 45.0,
        "badge_color": "#ff7f0e"
    },
    "Moderately Aggressive": {
        "range": (60.0, 80.0),
        "description": "Capital appreciation over a long horizon; resilient to significant interim drawdowns.",
        "max_equity_pct": 75.0,
        "recommended_cash_bond_pct": 25.0,
        "badge_color": "#d62728"
    },
    "Aggressive": {
        "range": (80.0, 100.0),
        "description": "Maximum long-term wealth compounding; accepts substantial volatility for higher equity risk premia.",
        "max_equity_pct": 95.0,
        "recommended_cash_bond_pct": 5.0,
        "badge_color": "#9467bd"
    }
}

def get_risk_tier(score: float) -> str:
    """Maps a continuous risk score (0-100) to standard 5-tier classification."""
    s = float(np.clip(score, 0.0, 100.0))
    if s <= 20.0:
        return "Very Conservative"
    elif s <= 40.0:
        return "Conservative"
    elif s <= 60.0:
        return "Moderate"
    elif s <= 80.0:
        return "Moderately Aggressive"
    else:
        return "Aggressive"


def compute_financial_risk_capacity(
    income: float,
    networth: float,
    liquid_savings: float = None,
    debt: float = None,
    kids: int = 0,
    age: int = 45,
    occupation: int = 1,
    investment_horizon: int = 10,
    wsaved: int = 2,
    currency: str = "USD"
) -> dict:
    """
    Computes Financial Risk Capacity (0 - 100).
    Measures the investor's balance sheet ability to absorb capital loss without compromising standard of living.
    """
    # Guard against positional argument mixups for wsaved vs currency
    if isinstance(wsaved, str) and wsaved.upper() in ["USD", "INR"]:
        currency = wsaved.upper()
        wsaved = 2
        
    inc = max(0.0, float(income))
    nw = float(networth)
    kids = max(0, int(kids))
    age = max(18, min(100, int(age)))
    horizon = max(1, min(40, int(investment_horizon)))
    
    # Currency scaling benchmarks
    if currency == "INR":
        # INR scales: typical income ₹2L to ₹1Cr, networth ₹0 to ₹10Cr
        norm_inc = 0.0 if inc <= 0 else np.clip((np.log10(max(1.0, inc)) - 4.5) / (7.0 - 4.5), 0.0, 1.0)
        norm_nw = 0.0 if nw <= 0 else np.clip((np.log10(max(1.0, nw)) - 5.0) / (8.0 - 5.0), 0.0, 1.0)
        
        # Savings default: 20% of networth or 3 months income
        if liquid_savings is None:
            liquid_savings = max(0.0, nw * 0.15) if nw > 0 else (inc * 0.25)
        norm_sav = 0.0 if liquid_savings <= 0 else np.clip((np.log10(max(1.0, liquid_savings)) - 4.0) / (6.5 - 4.0), 0.0, 1.0)
        
        debt_val = 0.0 if debt is None else max(0.0, float(debt))
        assets = max(1.0, max(0.0, nw) + debt_val)
        leverage = debt_val / assets if assets > 0 else 1.0
    else:
        # USD scales: income $10k to $2M, networth $0 to $5M
        norm_inc = 0.0 if inc <= 0 else np.clip((np.log10(max(1.0, inc)) - 4.0) / (6.3 - 4.0), 0.0, 1.0)
        norm_nw = 0.0 if nw <= 0 else np.clip((np.log10(max(1.0, nw)) - 4.0) / (6.7 - 4.0), 0.0, 1.0)
        
        if liquid_savings is None:
            liquid_savings = max(0.0, nw * 0.15) if nw > 0 else (inc * 0.25)
        norm_sav = 0.0 if liquid_savings <= 0 else np.clip((np.log10(max(1.0, liquid_savings)) - 3.5) / (6.0 - 3.5), 0.0, 1.0)
        
        debt_val = 0.0 if debt is None else max(0.0, float(debt))
        assets = max(1.0, max(0.0, nw) + debt_val)
        leverage = debt_val / assets if assets > 0 else 1.0

    # 1. Income Component (0 - 30 pts)
    inc_pts = norm_inc * 30.0
    
    # 2. Net Worth Component (0 - 35 pts) - Accumulated wealth gives capacity even if income is zero!
    nw_pts = norm_nw * 35.0
    
    # 3. Liquidity / Emergency Buffer (0 - 15 pts)
    sav_pts = norm_sav * 15.0
    
    # 4. Employment Stability (0 - 10 pts)
    # 1: Manager/Prof, 2: Tech/Sales, 3: Craft/Prod, 4: Unemployed/Retired
    occ_map = {1: 10.0, 2: 7.5, 3: 5.0, 4: 1.0}
    occ_pts = occ_map.get(int(occupation), 5.0)
    
    # 5. Investment Horizon & Age Lifecycle (0 - 10 pts)
    horizon_factor = np.clip(horizon / 25.0, 0.0, 1.0)
    age_factor = np.clip((75.0 - age) / 50.0, 0.0, 1.0)
    horizon_pts = (0.6 * horizon_factor + 0.4 * age_factor) * 10.0
    
    # Penalties
    debt_penalty = min(15.0, leverage * 20.0)
    kids_penalty = min(kids, 4) * 2.5
    
    # Savings behavior bonus/penalty
    wsaved_map = {1: -5.0, 2: 0.0, 3: 5.0} # 1: spent > inc, 2: spent = inc, 3: saved
    wsaved_adj = wsaved_map.get(int(wsaved), 0.0)
    
    raw_capacity = inc_pts + nw_pts + sav_pts + occ_pts + horizon_pts + wsaved_adj - debt_penalty - kids_penalty
    capacity_score = float(np.clip(raw_capacity, 3.0, 98.0))
    
    # Financial Stability Score (0 - 100) measures balance sheet health
    # Combines net worth, income coverage, low debt, emergency savings
    solvency_score = 100.0 * (1.0 - min(1.0, leverage))
    stability_score = float(np.clip(0.35 * solvency_score + 0.35 * (nw_pts / 35.0 * 100.0) + 0.30 * (sav_pts / 15.0 * 100.0), 5.0, 99.0))
    
    # Explainability Factor Lists
    supporting_factors = []
    caution_factors = []
    
    curr_sym = "₹" if currency == "INR" else "$"
    
    if inc >= (1000000 if currency == "INR" else 150000):
        supporting_factors.append(f"Strong annual cash flow ({curr_sym}{inc:,.0f}) supports loss absorption.")
    elif inc <= 0:
        caution_factors.append(f"Zero current earned income restricts ongoing capital replenishment.")
    elif inc < (300000 if currency == "INR" else 40000):
        caution_factors.append(f"Modest annual earnings ({curr_sym}{inc:,.0f}) limits loss absorption buffer.")
        
    if nw >= (20000000 if currency == "INR" else 1500000):
        supporting_factors.append(f"Substantial net worth ({curr_sym}{nw:,.0f}) provides large balance sheet cushion.")
    elif nw <= 0:
        caution_factors.append(f"Negligible or zero accumulated net worth ({curr_sym}{nw:,.0f}) offers no financial buffer.")
        
    if liquid_savings >= (500000 if currency == "INR" else 50000):
        supporting_factors.append(f"Robust liquid emergency reserves ({curr_sym}{liquid_savings:,.0f}) prevent forced asset liquidation.")
    else:
        caution_factors.append(f"Limited emergency liquid savings ({curr_sym}{liquid_savings:,.0f}).")
        
    if leverage > 0.40:
        caution_factors.append(f"Elevated debt-to-assets leverage ({leverage*100:.1f}%) reduces risk capacity.")
    elif debt_val <= 0 or leverage < 0.15:
        supporting_factors.append(f"Low or zero debt burden provides clean balance sheet freedom.")
        
    if kids >= 2:
        caution_factors.append(f"Multiple financial dependents ({kids} dependents) require defensive liquidity.")
    elif kids == 0:
        supporting_factors.append("No dependent child obligations reduces nondiscretionary cash outflows.")
        
    if horizon >= 15:
        supporting_factors.append(f"Long investment horizon ({horizon} years) provides multi-year recovery window.")
    elif horizon <= 3:
        caution_factors.append(f"Short investment horizon ({horizon} years) necessitates capital preservation.")
        
    return {
        "capacity_score": round(capacity_score, 2),
        "stability_score": round(stability_score, 2),
        "inc_pts": round(inc_pts, 2),
        "nw_pts": round(nw_pts, 2),
        "sav_pts": round(sav_pts, 2),
        "occ_pts": round(occ_pts, 2),
        "horizon_pts": round(horizon_pts, 2),
        "debt_penalty": round(debt_penalty, 2),
        "kids_penalty": round(kids_penalty, 2),
        "supporting_factors": supporting_factors,
        "caution_factors": caution_factors
    }


def compute_psychological_risk_willingness(
    risk_willingness_scale: int = 2,
    downturn_reaction: int = 2,
    education: int = 3,
    age: int = 45,
    horizon: int = 10
) -> dict:
    """
    Computes Psychological Risk Willingness (0 - 100).
    Measures cognitive and emotional comfort with volatility, drawdowns, and uncertainty.
    Independent of wealth or income.
    """
    # 1. Stated Risk Willingness (1 to 4)
    # 1: Substantial Risk, 2: Above Average, 3: Average, 4: Not Willing
    base_map = {1: 88.0, 2: 66.0, 3: 45.0, 4: 15.0}
    w_base = base_map.get(int(risk_willingness_scale), 45.0)
    
    # 2. Market Downturn Reaction (1 to 4)
    # 1: Buy aggressively on dips (+8), 2: Hold steady (0), 3: Feel anxious / sell some (-8), 4: Panic sell to cash (-16)
    react_map = {1: 8.0, 2: 0.0, 3: -8.0, 4: -16.0}
    react_pts = react_map.get(int(downturn_reaction), 0.0)
    
    # 3. Education & Financial Sophistication (1 to 4)
    ed_map = {1: -4.0, 2: 0.0, 3: 3.0, 4: 6.0}
    ed_pts = ed_map.get(int(education), 0.0)
    
    # 4. Behavioral Horizon Adjustment
    # Investors planning for >15 years have longer behavioral patience
    horizon_adj = 4.0 if horizon >= 15 else (-4.0 if horizon <= 3 else 0.0)
    
    raw_willingness = w_base + react_pts + ed_pts + horizon_adj
    willingness_score = float(np.clip(raw_willingness, 4.0, 98.0))
    
    return {
        "willingness_score": round(willingness_score, 2),
        "w_base": w_base,
        "react_pts": react_pts,
        "ed_pts": ed_pts,
        "horizon_adj": horizon_adj,
        "tier": get_risk_tier(willingness_score)
    }


def evaluate_final_risk_profile(
    income: float,
    networth: float,
    liquid_savings: float = None,
    debt: float = None,
    kids: int = 0,
    age: int = 45,
    education: int = 3,
    marital_status: int = 1,
    occupation: int = 1,
    risk_willingness_scale: int = 2,
    downturn_reaction: int = 2,
    investment_horizon: int = 10,
    wsaved: int = 2,
    currency: str = "USD",
    capacity_weight: float = 0.35,
    willingness_weight: float = 0.65
) -> dict:
    """
    Synthesizes Financial Risk Capacity and Psychological Risk Willingness into an academically defensible,
    fiduciary-compliant final investor risk profile.
    """
    # Guard against positional argument mixups for wsaved vs currency
    if isinstance(wsaved, str) and wsaved.upper() in ["USD", "INR"]:
        currency = wsaved.upper()
        wsaved = 2
    # 1. Compute Two Dimensions
    cap_res = compute_financial_risk_capacity(
        income=income,
        networth=networth,
        liquid_savings=liquid_savings,
        debt=debt,
        kids=kids,
        age=age,
        occupation=occupation,
        investment_horizon=investment_horizon,
        wsaved=wsaved,
        currency=currency
    )
    
    will_res = compute_psychological_risk_willingness(
        risk_willingness_scale=risk_willingness_scale,
        downturn_reaction=downturn_reaction,
        education=education,
        age=age,
        horizon=investment_horizon
    )
    
    cap_score = cap_res["capacity_score"]
    will_score = will_res["willingness_score"]
    
    # 2. Calibrated Base Composite
    composite_score = (capacity_weight * cap_score) + (willingness_weight * will_score)
    
    # 3. Asymmetric Fiduciary Constraint Application
    constraint_applied = None
    final_score = composite_score
    
    # Rule 1: Capacity Ceiling (Low financial capacity strictly bounds aggressive risk)
    if cap_score < 25.0:
        max_allowed = cap_score + 5.0
        if composite_score > max_allowed:
            final_score = max_allowed
            constraint_applied = (
                "FIDUCIARY CAPACITY CEILING TRIGGERED: High psychological willingness "
                "was strictly constrained by low financial capacity to protect against irreversible financial insolvency."
            )
    elif cap_score < 40.0:
        max_allowed = cap_score + 15.0
        if composite_score > max_allowed:
            final_score = max_allowed
            constraint_applied = (
                "FINANCIAL CAPACITY GATING TRIGGERED: Recommendation capped to Moderate tier "
                "due to limited balance sheet resilience."
            )
            
    # Rule 2: Willingness Governor (Wealthy investor with low willingness is never forced into equity risk)
    if will_score < 25.0:
        max_allowed = will_score + 8.0
        if final_score > max_allowed:
            final_score = max_allowed
            constraint_applied = (
                "WILLINGNESS GOVERNOR TRIGGERED: Despite strong financial capacity, "
                "the recommendation was moderated to respect the investor's conservative risk preference and loss aversion."
            )
            
    final_score = float(np.clip(final_score, 1.0, 99.0))
    risk_category = get_risk_tier(final_score)
    cat_meta = RISK_CATEGORIES[risk_category]
    
    # 4. Markowitz Risk Aversion Lambda Mapping
    # High score (100) -> Low lambda (~0.5); Low score (0) -> High lambda (~12.5)
    risk_aversion_lambda = round(float((100.0 - final_score + 1.0) / 8.0), 3)
    
    # 5. Explanatory Narrative
    explanation = (
        f"Investor assessed with Financial Risk Capacity of {cap_score:.1f}/100 and "
        f"Psychological Risk Willingness of {will_score:.1f}/100. "
        f"The synthesized risk tolerance score is {final_score:.1f}/100, placing the portfolio in the "
        f"'{risk_category}' category."
    )
    if constraint_applied:
        explanation += f" Note: {constraint_applied}"
        
    return {
        "final_risk_score": round(final_score, 2),
        "risk_category": risk_category,
        "financial_capacity_score": cap_score,
        "psychological_willingness_score": will_score,
        "financial_stability_score": cap_res["stability_score"],
        "risk_aversion_lambda": risk_aversion_lambda,
        "max_equity_allocation": cat_meta["max_equity_pct"],
        "recommended_cash_bond_allocation": cat_meta["recommended_cash_bond_pct"],
        "recommended_equity_allocation": 100.0 - cat_meta["recommended_cash_bond_pct"],
        "badge_color": cat_meta["badge_color"],
        "constraint_applied": constraint_applied,
        "explanation": explanation,
        "supporting_factors": cap_res["supporting_factors"],
        "caution_factors": cap_res["caution_factors"],
        "capacity_breakdown": {
            "Income Component": cap_res["inc_pts"],
            "Net Worth Component": cap_res["nw_pts"],
            "Liquidity Component": cap_res["sav_pts"],
            "Employment Component": cap_res["occ_pts"],
            "Horizon Component": cap_res["horizon_pts"],
            "Debt Penalty": -cap_res["debt_penalty"],
            "Dependents Penalty": -cap_res["kids_penalty"]
        }
    }


if __name__ == "__main__":
    test_profile = evaluate_final_risk_profile(
        income=125000,
        networth=500000,
        liquid_savings=75000,
        debt=40000,
        kids=2,
        age=45,
        risk_willingness_scale=2,
        currency="USD"
    )
    print("Sample Assessment Result:")
    for k, v in test_profile.items():
        if k != "capacity_breakdown":
            print(f"  {k}: {v}")
