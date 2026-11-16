"""
Automated Test Suite for Logical Investor Risk Tolerance Scenarios
Validates that the Robo-Advisor risk assessment and portfolio engine adhere to core financial principles:
TEST 1: Increasing Income Monotonicity
TEST 2: Zero Income & Zero Wealth (Broke Profile) Fiduciary Protection
TEST 3: Zero Income with High Wealth Preservation of Capacity
TEST 4: High Income with Low Risk Willingness (Conservative Preference)
TEST 5: Low Income with High Willingness (Capacity Gating / Fiduciary Cap)
TEST 6: High Income and High Willingness (Aggressive Alignment)
"""

import os
import sys
import pytest

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.risk_assessment import (
    evaluate_final_risk_profile,
    compute_financial_risk_capacity,
    compute_psychological_risk_willingness,
    get_risk_tier
)


def test_scenario_1_increasing_income():
    """
    TEST 1: Increasing Income
    Keep all other relevant characteristics constant.
    Investor A: Annual income ₹2 lakh.
    Investor B: Annual income ₹10 lakh.
    Investor C: Annual income ₹25 lakh.
    Expected:
    - Financial risk capacity improves strictly monotonically as income increases.
    - Psychological risk willingness remains unchanged.
    """
    incomes = [200000, 1000000, 2500000]
    results = [
        evaluate_final_risk_profile(
            income=inc,
            networth=1500000,
            liquid_savings=300000,
            debt=200000,
            kids=1,
            age=35,
            occupation=1,
            risk_willingness_scale=2,
            currency="INR"
        )
        for inc in incomes
    ]
    
    cap_a, cap_b, cap_c = [r["financial_capacity_score"] for r in results]
    will_a, will_b, will_c = [r["psychological_willingness_score"] for r in results]
    final_a, final_b, final_c = [r["final_risk_score"] for r in results]
    
    # 1. Capacity must increase strictly as income increases
    assert cap_a < cap_b < cap_c, f"Expected strictly increasing capacity: {cap_a} < {cap_b} < {cap_c}"
    
    # 2. Psychological willingness must remain identical
    assert will_a == will_b == will_c, f"Expected willingness unchanged: {will_a}, {will_b}, {will_c}"
    
    # 3. Final risk score must also increase or stay non-decreasing
    assert final_a <= final_b <= final_c, f"Expected non-decreasing final score: {final_a} <= {final_b} <= {final_c}"
    
    print(f"\n[PASS] TEST 1 Increasing Income: Cap ₹2L={cap_a:.1f} < ₹10L={cap_b:.1f} < ₹25L={cap_c:.1f} | Will={will_a:.1f}")


def test_scenario_2_zero_income_and_zero_wealth():
    """
    TEST 2: Zero Income & Zero Wealth
    Investor:
    - Annual income: ₹0.
    - Net worth: ₹0.
    - Savings: ₹0.
    - Outstanding debt: High (₹5 lakh).
    - Dependents: Multiple (3 kids).
    Expected:
    - Low financial risk capacity.
    - Conservative or Very Conservative final recommendation.
    """
    result = evaluate_final_risk_profile(
        income=0,
        networth=0,
        liquid_savings=0,
        debt=500000,
        kids=3,
        age=32,
        occupation=4, # Unemployed
        risk_willingness_scale=2, # Even with average/above-average willingness
        currency="INR"
    )
    
    cap = result["financial_capacity_score"]
    cat = result["risk_category"]
    final = result["final_risk_score"]
    
    # Capacity must be extremely low (< 20)
    assert cap <= 20.0, f"Expected low capacity for broke investor, got {cap}"
    
    # Final recommendation must be Very Conservative or Conservative
    assert cat in ["Very Conservative", "Conservative"], f"Expected conservative tier, got {cat} ({final})"
    
    # Fiduciary constraint must trigger to protect broke investor
    assert result["constraint_applied"] is not None
    
    print(f"\n[PASS] TEST 2 Zero Income & Wealth: Cap={cap:.1f}, Final={final:.1f}, Tier={cat}")


def test_scenario_3_zero_income_with_high_wealth():
    """
    TEST 3: Zero Income With High Wealth
    Investor:
    - Annual income: ₹0.
    - Net worth: ₹5 crore (₹50,000,000).
    - Liquid savings: Substantial (₹50 lakh).
    - Debt: Low (₹0).
    Expected:
    - The investor should NOT automatically be classified as having low financial risk capacity.
    - Significant balance sheet resilience should be recognized.
    """
    result = evaluate_final_risk_profile(
        income=0,
        networth=50000000,
        liquid_savings=5000000,
        debt=0,
        kids=0,
        age=55,
        occupation=4, # Retired
        risk_willingness_scale=2,
        currency="INR"
    )
    
    cap = result["financial_capacity_score"]
    cat = result["risk_category"]
    
    # Capacity must be robust (> 45) due to ₹5 crore assets
    assert cap >= 45.0, f"Expected high wealth to support capacity >= 45, got {cap}"
    assert cat not in ["Very Conservative"], f"High wealth investor should not be Very Conservative solely due to 0 income, got {cat}"
    
    print(f"\n[PASS] TEST 3 Zero Income High Wealth: Cap={cap:.1f}, Final={result['final_risk_score']:.1f}, Tier={cat}")


def test_scenario_4_high_income_low_willingness():
    """
    TEST 4: High Income but Low Risk Willingness
    Investor:
    - Annual income: ₹50 lakh (₹5,000,000).
    - High net worth (₹2 crore).
    - Low willingness to accept losses (scale 4, panic sell reaction).
    - Conservative investment preference.
    Expected:
    - High financial capacity, but low psychological willingness.
    - Final recommendation is Conservative or Very Conservative (respecting investor preference).
    """
    result = evaluate_final_risk_profile(
        income=5000000,
        networth=20000000,
        liquid_savings=2000000,
        debt=0,
        kids=1,
        age=45,
        occupation=1,
        risk_willingness_scale=4, # Not willing to take any financial risk
        downturn_reaction=4,      # Panic sell to cash
        currency="INR"
    )
    
    cap = result["financial_capacity_score"]
    will = result["psychological_willingness_score"]
    cat = result["risk_category"]
    
    assert cap >= 70.0, f"Expected high capacity >= 70, got {cap}"
    assert will <= 25.0, f"Expected low willingness <= 25, got {will}"
    assert cat in ["Very Conservative", "Conservative"], f"Expected conservative tier, got {cat}"
    assert result["constraint_applied"] is not None
    
    print(f"\n[PASS] TEST 4 High Inc Low Will: Cap={cap:.1f}, Will={will:.1f}, Final={result['final_risk_score']:.1f}, Tier={cat}")


def test_scenario_5_low_income_high_willingness():
    """
    TEST 5: Low Income but High Risk Willingness
    Investor:
    - Annual income: ₹3 lakh (₹300,000).
    - Limited savings (₹50,000).
    - High psychological willingness to take risks (scale 1, aggressive reaction).
    Expected:
    - System recognizes high willingness (> 80).
    - System limits final recommendation according to financial capacity (gated to Conservative or Moderate).
    """
    result = evaluate_final_risk_profile(
        income=300000,
        networth=200000,
        liquid_savings=50000,
        debt=150000,
        kids=2,
        age=26,
        occupation=2,
        risk_willingness_scale=1, # Substantial risk
        downturn_reaction=1,      # Buy more
        currency="INR"
    )
    
    cap = result["financial_capacity_score"]
    will = result["psychological_willingness_score"]
    cat = result["risk_category"]
    final = result["final_risk_score"]
    
    assert will >= 80.0, f"Expected high willingness >= 80, got {will}"
    assert cap <= 30.0, f"Expected limited capacity <= 30, got {cap}"
    
    # Must NOT produce Aggressive recommendation because financial capacity is fragile!
    assert cat in ["Very Conservative", "Conservative", "Moderate"], f"Final tier must be limited by capacity, got {cat}"
    assert result["constraint_applied"] is not None
    
    print(f"\n[PASS] TEST 5 Low Inc High Will: Will={will:.1f} recognized, but Final={final:.1f} capped by Cap={cap:.1f} -> Tier={cat}")


def test_scenario_6_high_income_and_high_willingness():
    """
    TEST 6: High Income and High Risk Willingness
    Investor:
    - High income: ₹50 lakh.
    - High net worth: ₹3 crore.
    - Low debt: ₹0.
    - Long investment horizon: 20 years.
    - High willingness to accept losses (scale 1).
    Expected:
    - Aggressive or Moderately Aggressive recommendation.
    """
    result = evaluate_final_risk_profile(
        income=5000000,
        networth=30000000,
        liquid_savings=5000000,
        debt=0,
        kids=0,
        age=32,
        occupation=1,
        risk_willingness_scale=1,
        downturn_reaction=1,
        investment_horizon=20,
        currency="INR"
    )
    
    cap = result["financial_capacity_score"]
    will = result["psychological_willingness_score"]
    cat = result["risk_category"]
    final = result["final_risk_score"]
    
    assert cap >= 75.0, f"Expected high capacity >= 75, got {cap}"
    assert will >= 85.0, f"Expected high willingness >= 85, got {will}"
    assert cat in ["Moderately Aggressive", "Aggressive"], f"Expected aggressive tier, got {cat}"
    assert final >= 75.0, f"Expected final score >= 75, got {final}"
    
    print(f"\n[PASS] TEST 6 High Inc & High Will: Cap={cap:.1f}, Will={will:.1f}, Final={final:.1f}, Tier={cat}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
