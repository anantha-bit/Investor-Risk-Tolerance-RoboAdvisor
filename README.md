# Modeling Investor Risk Tolerance and Enabling a Machine Learning–Based Robo-Advisor

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Robo--Advisor-FF4B4B.svg)](app.py)
[![PES University](https://img.shields.io/badge/PES%20University-UE24AM320A%20Capstone%20Phase--1-navy.svg)](reports/)

> **5th-Semester Capstone Project Phase - 1 (UE24AM320A)**  
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

## Executive Overview
The quantification of an investor’s risk tolerance is the primary determinant of portfolio asset allocation and capital preservation. However, commercial wealth management and first-generation robo-advisors rely on **subjective Risk Tolerance Questionnaires (RTQs)**. As established in behavioral economics, human investors suffer from psychological biases: they overestimate their risk appetite during bull markets and capitulate to irrational panic-selling during crashes.

This project delivers an end-to-end data-driven machine learning system that:
1. **Mines Empirical Ground Truth:** Leverages the **Federal Reserve Board’s Survey of Consumer Finances (SCF) 2007–2009 Longitudinal Panel Dataset** to track how households reacted across the 2008 Lehman collapse and Great Financial Crisis.
2. **Isolates Intelligent Investors:** Filters for disciplined households whose S&P 500-normalized asset allocation changed by $\le 10\%$, establishing an objective target metric: **True Risk Tolerance**.
3. **Benchmarks 5 Machine Learning Frameworks:** Trains, tunes, and evaluates **XGBoost**, **Keras (Deep MLP)**, **PyTorch with FastAI**, **PyTorch with TabNet**, and **PyTorch Lightning**.
4. **Evaluates Multi-Criteria Performance:** Assesses models across standard quantitative metrics (RMSE, MAE, R², MSE, latency) as well as the three case-study dimensions: **Simplicity**, **Transparency**, and **Efficacy**.
5. **Enables a Live Robo-Advisor Dashboard:** Replicates the Figure 5-6 web interface in **Streamlit**, linking predicted risk tolerance dynamically to **Markowitz Modern Portfolio Theory (MPT) Mean-Variance Asset Allocation** and historical $100 backtest growth trajectories.

---

## System Architecture

```
                                  [ Federal Reserve Board SCF 2007-2009 Panel ]
                                                        │
                                                        ▼
                                       [ Longitudinal Data Preprocessing ]
                                    • Liquid Risky vs Risk-Free Separation
                                    • S&P 500 Crisis Normalization (1478 -> 948)
                                    • Intelligent Investor Filter (|ΔRT| ≤ 10%)
                                    • Ground Truth Target: TrueRiskTol (0-100)
                                                        │
                                                        ▼
                        ┌───────────────────────────────────────────────────────────────┐
                        │              5-Framework Regression Engine                    │
                        │  1. XGBoost (Gradient Boosted Trees)                         │
                        │  2. Keras (Deep MLP with Torch backend)                       │
                        │  3. PyTorch FastAI (Tabular Embeddings & One-Cycle)           │
                        │  4. PyTorch TabNet (Self-Attentive Sparse Masks)              │
                        │  5. PyTorch Lightning (Modular Tabular Regressor)             │
                        └───────────────────────────────┬───────────────────────────────┘
                                                        │ Champion Model: XGBoost
                                                        │ (R² = 0.9537, RMSE = 3.46)
                                                        ▼
                                      [ Markowitz MPT Optimization Engine ]
                                     • Dynamic Risk Aversion: λ(RT) = (101 - RT) / 8.5
                                     • SLSQP Constrained Quadratic Utility Solver
                                     • Historical Backtest of $100 Investment
                                                        │
                                                        ▼
                                      [ Full-Stack Robo-Advisor Dashboard ]
                                    Step 1: Enter Demographic & Financial Traits
                                    Step 2: Real-Time Allocation & $100 Backtest
```

---

## Quantitative Benchmark Results

Evaluated on the identical 20% holdout test partition ($N = 962$):

| Framework | RMSE ↓ | MAE ↓ | $R^2$ Score ↑ | MSE ↓ | Training Time | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Champion)** | **3.4648** | **1.9063** | **0.9537** | **12.0048** | **0.70 s** | **0.20 ms** |
| **Keras (Deep MLP)** | 7.4283 | 3.8284 | 0.7871 | 55.1804 | 19.22 s | 0.36 ms |
| **PyTorch FastAI** | 8.4073 | 4.5604 | 0.7273 | 70.6820 | 4.81 s | 0.65 ms |
| **PyTorch TabNet** | 9.2111 | 4.5070 | 0.6727 | 84.8450 | 39.51 s | 1.13 ms |
| **PyTorch Lightning** | 8.6479 | 4.2456 | 0.7115 | 74.7857 | 14.31 s | **0.04 ms** |

---

## Qualitative Comparison: Simplicity, Transparency, Efficacy

| Dimension | Evaluation Criteria | XGBoost | Keras | FastAI | TabNet | Lightning |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Simplicity** | Code brevity, native handling of missing values, zero scaling overhead | **9.2 / 10** | 8.0 / 10 | 8.5 / 10 | 7.5 / 10 | 7.8 / 10 |
| **Transparency** | Model explainability, Gini split inspection, attention masks, TreeSHAP | **9.0 / 10** | 6.0 / 10 | 6.5 / 10 | 8.8 / 10 | 6.2 / 10 |
| **Efficacy** | Predictive generalization on unseen tabular data, resilience to outliers | **9.5 / 10** | 8.2 / 10 | 8.5 / 10 | 8.6 / 10 | 8.3 / 10 |

---

## Repository Structure

```
Investor-Risk-Tolerance-RoboAdvisor/
├── data/
│   ├── InputData.csv                       # Clean preprocessed SCF modeling dataset (4,810 records)
│   ├── SP500Data.csv                       # Historical S&P 500 stock prices for portfolio optimization
│   └── SCFP2009panel.xlsx                  # Raw Federal Reserve SCF 2009 panel dataset (optional)
├── src/
│   ├── download_data.py                    # Automated dataset acquisition script
│   ├── preprocess_scf.py                   # Econometric data pipeline & intelligent investor filtering
│   ├── eda.py                              # Exploratory data analysis & statistical generation
│   ├── train_models.py                     # 5-framework benchmark & quantitative evaluation
│   ├── portfolio_optimization.py           # Markowitz MPT Mean-Variance optimizer & backtester
│   ├── generate_report.py                  # Generates PES-compliant Word & PDF academic report
│   ├── generate_presentation.py            # Generates executive & academic PowerPoint presentation
│   └── generate_notebooks.py               # Generates clean, reproducible Jupyter notebooks
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
│   ├── model_radar_evaluation.png
│   ├── actual_vs_predicted_all_models.png
│   └── feature_importance_xgboost.png
├── reports/
│   ├── UE24AM320A_Capstone_Phase1_Report.docx  # Full Academic Capstone Phase-1 Report (Word)
│   ├── UE24AM320A_Capstone_Phase1_Report.pdf   # Full Academic Capstone Phase-1 Report (PDF)
│   ├── Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx # Presentation Slide Deck
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

### 2. Launch the Interactive Robo-Advisor Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Re-run Pipelines
- **Data Preprocessing:** `python src/preprocess_scf.py`
- **Exploratory Data Analysis:** `python src/eda.py`
- **Train & Benchmark 5 Frameworks:** `python src/train_models.py`
- **Generate Academic Report (.docx & .pdf):** `python src/generate_report.py`
- **Generate Presentation Slide Deck (.pptx):** `python src/generate_presentation.py`

---

## Deliverables Summary
- **Word Dissertation:** [`reports/UE24AM320A_Capstone_Phase1_Report.docx`](reports/UE24AM320A_Capstone_Phase1_Report.docx)
- **PDF Dissertation:** [`reports/UE24AM320A_Capstone_Phase1_Report.pdf`](reports/UE24AM320A_Capstone_Phase1_Report.pdf)
- **Presentation Deck:** [`reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx`](reports/Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx)
- **Viva Voce Defense Guide:** [`VIVA_PREPARATION_GUIDE.md`](VIVA_PREPARATION_GUIDE.md)

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
