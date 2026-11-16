# Modeling Investor Risk Tolerance and Enabling an ML-Based Robo-Advisor

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Robo--Advisor-FF4B4B.svg)](app.py)
[![Pytest](https://img.shields.io/badge/Tests-6%20Passed-brightgreen.svg)](tests/test_logical_scenarios.py)
[![PES University](https://img.shields.io/badge/PES%20University-MLBD%20Mini%20Project-navy.svg)](reports/)

> **Machine Learning for Big Data (MLBD) — Mini Project**  
> **Department of Computer Science and Engineering (AI & ML)**  
> **Faculty of Engineering, PES University, Bengaluru**  
> **Academic Period:** August – December 2026

---

## Project Team Members
| Student Name | SRN | Department / Program |
| :--- | :--- | :--- |
| **Ananthakrishna M A** | **PES1UG24AM036** | B.Tech CSE (AI & ML) |
| **Akash G K** | **PES1UG24AM022** | B.Tech CSE (AI & ML) |
| **Amar Patil** | **PES1UG24AM031** | B.Tech CSE (AI & ML) |
| **Chandraraj Patil** | **PES1UG24AM425** | B.Tech CSE (AI & ML) |

---

## Executive Overview & Architectural Upgrade

In commercial wealth management and robo-advisory platforms, assessing an investor's risk tolerance is the foundational prerequisite for asset allocation and capital preservation. However, first-generation machine learning implementations (such as the textbook case study by Hariom Tatsath) suffered from severe methodological defects that produced contradictory and dangerous investment advice:

- **Contradiction 1 (Income Inversion):** Increasing an investor's annual income would sometimes decrease their predicted risk tolerance.
- **Contradiction 2 (Zero-Income Anomaly):** Broke investors with ₹0 income, ₹0 net worth, and multiple dependents received high risk tolerance scores and aggressive equity allocations.
- **Contradiction 3 (Age Conflation):** The legacy target variable ($Risky / Total Liquid Assets$) had a massive **-0.7049 correlation with Age**, causing young destitute investors to appear aggressive while wealthy older investors appeared near-zero.
- **Contradiction 4 (Disregarded Risk Willingness):** Self-reported risk willingness (`RISK07`) was virtually ignored by tree models (5% feature importance) and had an inverted non-monotonic response.

### The Solution: Dual-Dimension Risk Profiling Engine
This project comprehensively redesigns the methodology by decoupling risk tolerance into two academically grounded, regulatory-aligned dimensions (FINRA Rule 2111 / CFA Institute standards):
1. **Financial Risk Capacity (Objective Ability):** Evaluates balance sheet solvency, log-transformed annual income, accumulated net worth, liquid emergency reserves, debt leverage, family dependents, employment stability, and investment horizon.
2. **Psychological Risk Willingness (Subjective Tolerance):** Evaluates behavioral risk appetite, loss aversion, reaction to market crashes (20% drawdowns), education, and investment objectives—completely independent of wealth.
3. **Asymmetric Fiduciary Gating:** Enforces safety constraints so that high psychological willingness can **never** force a financially fragile investor into an aggressive equity allocation (Capacity Ceiling), while a wealthy risk-averse investor is never forced into volatile assets (Willingness Governor).

---

## System Architecture

```
                                  [ Federal Reserve Board SCF 2007-2009 Panel ]
                                                        │
                                                        ▼
                                        [ Longitudinal Data Preprocessing ]
                                     • Liquid Risky vs Risk-Free Asset Extraction
                                     • S&P 500 Crisis Normalization (1478 -> 948)
                                     • Intelligent Investor Filter (|ΔRT| ≤ 10%)
                                                        │
                                                        ▼
                        ┌───────────────────────────────────────────────────────────────┐
                        │             Dual-Dimension Risk Profiling Engine              │
                        │                                                               │
                        │  Dimension A: Financial Risk Capacity (35%)                   │
                        │  • Log Income, Log Net Worth, Liquid Savings, Debt Leverage,  │
                        │    Dependents (Kids), Employment Stability, Horizon           │
                        │                                                               │
                        │  Dimension B: Psychological Risk Willingness (65%)            │
                        │  • Surveyed Risk Appetite (RISK07), 20% Drawdown Reaction,    │
                        │    Education Level, Investment Experience                     │
                        │                                                               │
                        │  Fiduciary Constraint Gating:                                 │
                        │  • Capacity Ceiling: High Willingness capped if Capacity < 25 │
                        │  • Willingness Governor: High Capacity respects low appetite  │
                        └───────────────────────────────┬───────────────────────────────┘
                                                        │
                                                        ▼
                        ┌───────────────────────────────────────────────────────────────┐
                        │             5-Framework Supervised ML Benchmark               │
                        │  1. XGBoost (With Monotonic Constraints on Economic Features) │
                        │  2. Keras Deep Neural Network (PyTorch Backend)               │
                        │  3. PyTorch FastAI (Tabular Embeddings & One-Cycle Policy)    │
                        │  4. PyTorch TabNet (Self-Attentive Sparse Feature Masks)      │
                        │  5. PyTorch Lightning (Modular Structured Tabular Regressor)  │
                        └───────────────────────────────┬───────────────────────────────┘
                                                        │ Champion Model: XGBoost
                                                        │ (R² = 0.9918, RMSE = 1.74, Acc = 95.7%)
                                                        ▼
                                      [ Markowitz MPT Optimization Engine ]
                                     • Dynamic Risk Aversion: λ(RT) = (101 - RT) / 8.0
                                     • Two-Sleeve Allocation: Defensive Cash/Bonds (2.5%)
                                       + Mean-Variance Optimal Equities (SLSQP Solver)
                                     • Historical Backtest of $100 Investment
                                                        │
                                                        ▼
                                      [ Full-Stack Robo-Advisor Dashboard ]
                                    • Dual-Dimension Sliders (INR ₹ / USD $)
                                    • 5-Tier Category Badge & Financial Stability Score
                                    • "Why Did We Assign This Risk Profile?" Explainability
                                    • Mean-Variance Chart + $100 Growth Backtest Line
```

---

## Five Standard Risk Categories

| Risk Tier | Score Range | Description | Recommended Cash/Bonds | Max Equity Allocation |
| :--- | :---: | :--- | :---: | :---: |
| **Very Conservative** | $0.0 - 20.0$ | Capital preservation with minimal drawdown risk | **75% - 85%** | **20%** |
| **Conservative** | $20.1 - 40.0$ | Income with capital defense; low market drawdown tolerance | **60% - 70%** | **35%** |
| **Moderate** | $40.1 - 60.0$ | Balanced capital appreciation and preservation | **40% - 50%** | **55%** |
| **Moderately Aggressive** | $60.1 - 80.0$ | Long-term capital growth; accepts cyclical market drawdowns | **20% - 30%** | **75%** |
| **Aggressive** | $80.1 - 100.0$ | Maximum compounding; high equity risk premium capture | **5% - 15%** | **95%** |

---

## Automated Test Cases & Scenario Validations

Automated unit and integration tests are implemented in [`tests/test_logical_scenarios.py`](tests/test_logical_scenarios.py). All 6 scenarios pass:

```bash
pytest -v tests/test_logical_scenarios.py
```

### Scenario Test Results:

| Scenario | Input Investor Profile | Financial Capacity | Psychological Willingness | Final Risk Score | Assigned Category | Fiduciary Constraint |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **TEST 1: Increasing Income** | Inc: ₹2L vs ₹10L vs ₹25L (all else constant) | **₹2L: 41.3<br>₹10L: 49.7<br>₹25L: 54.5** | **69.0<br>69.0<br>69.0** | **59.3<br>62.3<br>63.9** | **Moderate<br>Mod. Aggressive<br>Mod. Aggressive** | Monotonic capacity improvement; willingness unchanged |
| **TEST 2: Zero Income & Wealth** | Inc: ₹0, NW: ₹0, Debt: High (₹5L), 3 Kids | **3.0 / 100** | 69.0 / 100 | **8.0 / 100** | **Very Conservative** | **Capacity Ceiling:** High willingness suppressed by broke balance sheet |
| **TEST 3: Zero Income High Wealth** | Inc: ₹0, NW: ₹5 Crore, Debt: ₹0, Horizon: 15y | **51.5 / 100** | 69.0 / 100 | **62.9 / 100** | **Moderately Aggressive** | Capacity preserved via wealth; not penalized as broke |
| **TEST 4: High Income Low Willingness**| Inc: ₹50L, NW: ₹2 Crore, Debt: ₹0, Low Risk Appetite | **78.5 / 100** | **5.0 / 100** | **13.0 / 100** | **Very Conservative** | **Willingness Governor:** High wealth never forced into unwanted volatility |
| **TEST 5: Low Income High Willingness**| Inc: ₹3L, NW: ₹2L, Savings: ₹50k, Fearless Appetite | **17.4 / 100** | **98.0 / 100** | **22.4 / 100** | **Conservative** | **Capacity Ceiling:** Aggressive recommendation strictly capped to avoid insolvency |
| **TEST 6: High Income & Willingness** | Inc: ₹50L, NW: ₹3 Crore, Debt: ₹0, Long Horizon | **88.3 / 100** | **98.0 / 100** | **94.6 / 100** | **Aggressive** | Full dual alignment enables maximum equity growth |

---

## Quantitative Model Benchmarking Results

Evaluated on the 20% holdout test partition ($N = 962$):

| Framework | RMSE ↓ | MAE ↓ | $R^2$ Score ↑ | Tier Accuracy ↑ | Tier F1 ↑ | Train Time | Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Champion)** | **1.7429** | **1.1406** | **0.9918** | **95.74%** | **95.74%** | **1.01 s** | **0.22 ms** |
| **Keras (Deep MLP)** | 3.5241 | 2.1150 | 0.9663 | 88.77% | 88.46% | 23.56 s | 0.38 ms |
| **PyTorch FastAI** | 3.5476 | 2.1414 | 0.9659 | 89.09% | 88.84% | 21.20 s | 0.38 ms |
| **PyTorch Lightning** | 5.2574 | 3.5013 | 0.9251 | 87.73% | 87.46% | 8.94 s | **0.04 ms** |
| **PyTorch TabNet** | 5.6684 | 3.9726 | 0.9129 | 83.06% | 82.56% | 39.28 s | 1.11 ms |

### Monotonic Constraints in XGBoost:
XGBoost was trained with monotonic direction constraints:
```python
monotone_constraints = {
    'INCOME07': 1,      # Higher income cannot reduce risk capacity
    'NETWORTH07': 1,    # Higher net worth cannot reduce risk capacity
    'EDCL07': 1,        # Higher education cannot reduce risk capacity
    'KIDS07': -1,       # More dependents cannot increase risk capacity
    'RISK07': -1        # Higher numerical code (1->4) indicates lower willingness
}
```
This guarantees mathematical monotonicity and prevents tree overfitting anomalies.

---

## Repository Structure

```
Investor-Risk-Tolerance-RoboAdvisor/
├── data/
│   ├── InputData.csv                       # Clean enriched SCF modeling dataset (4,810 records)
│   ├── SP500Data.csv                       # Historical S&P 500 stock prices for portfolio optimization
│   └── SCFP2009panel.xlsx                  # Raw Federal Reserve SCF 2009 panel dataset
├── src/
│   ├── risk_assessment.py                  # Dual-dimension engine, capacity ceiling & explainability
│   ├── portfolio_optimization.py           # Markowitz MPT optimizer with defensive cash/bond sleeve
│   ├── preprocess_scf.py                   # Econometric data pipeline & target derivation
│   ├── train_models.py                     # 5-framework benchmark & monotonic XGBoost training
│   ├── eda.py                              # Exploratory data analysis & statistical generation
│   ├── generate_report.py                  # Generates Word & PDF academic report
│   ├── generate_presentation.py            # Generates PowerPoint presentation
│   └── generate_notebooks.py               # Generates reproducible Jupyter notebooks
├── tests/
│   └── test_logical_scenarios.py           # Automated test suite for all 6 logical scenarios
├── notebooks/
│   ├── 01_Data_Acquisition_and_Preprocessing.ipynb
│   ├── 02_Exploratory_Data_Analysis.ipynb
│   ├── 03_Regression_Frameworks_Benchmarking.ipynb
│   └── 04_Robo_Advisor_Portfolio_Optimization.ipynb
├── models/
│   ├── best_model.joblib                   # Serialized champion XGBoost model
│   ├── finalized_model.sav                 # Production model artifact for dashboard
│   ├── xgboost_model.json                  # Native XGBoost model file
│   ├── keras_model.keras                   # Keras deep neural network artifact
│   ├── fastai_learner.pkl                  # FastAI learner export
│   ├── tabnet_model.zip                    # PyTorch TabNet model weights
│   ├── lightning_tabular_model.pt          # PyTorch Lightning state dict
│   └── scaler.joblib                       # StandardScaler transformation artifact
├── visualizations/                         # High-resolution (300 DPI) publication figures
│   ├── eda_01_target_distribution.png
│   ├── eda_02_correlation_heatmap.png
│   ├── eda_03_demographics_vs_risk.png
│   ├── eda_04_financial_capacity.png
│   ├── eda_05_subjective_vs_revealed_risk.png
│   ├── eda_06_age_lifecycle_dynamics.png
│   ├── model_metrics_comparison.png
│   ├── actual_vs_predicted_all_models.png
│   └── feature_importance_xgboost.png
├── reports/
│   ├── MLBD_Project_Report.docx            # Full Academic MLBD Project Report
│   ├── MLBD_Project_Report.pdf             # Full Academic MLBD Project Report
│   ├── Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx # Slide Deck (PPTX)
│   ├── Investor_Risk_Tolerance_RoboAdvisor_Presentation.pdf  # Slide Deck (PDF)
│   ├── model_comparison_benchmark.csv      # Complete benchmark metric results table
│   └── eda_summary_statistics.csv          # Descriptive statistical summary table
├── app.py                                  # Full-Stack Interactive Streamlit Robo-Advisor Dashboard
├── VIVA_PREPARATION_GUIDE.md               # In-depth technical Viva Voce Q&A defense guide
├── requirements.txt                        # Python dependencies
└── README.md                               # Project documentation
```

---

## Quickstart & Installation

### 1. Clone Repository & Install Dependencies
```bash
git clone https://github.com/anantha-bit/Investor-Risk-Tolerance-RoboAdvisor.git
cd Investor-Risk-Tolerance-RoboAdvisor
pip install -r requirements.txt
```

### 2. Run Automated Test Suite
```bash
pytest -v tests/test_logical_scenarios.py
```

### 3. Launch the Interactive Robo-Advisor Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Re-run Pipelines
- **Data Preprocessing & Enrichment:** `python src/preprocess_scf.py`
- **Exploratory Data Analysis:** `python src/eda.py`
- **Train & Benchmark 5 Frameworks:** `python src/train_models.py`
- **Run Portfolio Optimization:** `python src/portfolio_optimization.py`

---

## Deliverables Summary
- **Word Project Report:** [`reports/MLBD_Project_Report.docx`](reports/MLBD_Project_Report.docx)
- **PDF Project Report:** [`reports/MLBD_Project_Report.pdf`](reports/MLBD_Project_Report.pdf)
- **Presentation Deck (PPTX):** [`reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx`](reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx)
- **Presentation Deck (PDF):** [`reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pdf`](reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pdf)
- **Viva Voce Defense Guide:** [`VIVA_PREPARATION_GUIDE.md`](VIVA_PREPARATION_GUIDE.md)

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
