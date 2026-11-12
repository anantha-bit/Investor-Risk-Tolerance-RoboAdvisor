# Comprehensive Viva Voce Preparation Guide
## Project: Modeling Investor Risk Tolerance and Enabling a Machine Learning–Based Robo-Advisor
**Course:** Machine Learning for Big Data (MLBD) — Mini Project  
**Department:** Computer Science and Engineering (AI & ML), PES University, Bengaluru  
**Team Members:**
- **Ananthakrishna M A** (PES1UG24AM036)
- **Akash G K** (PES1UG24AM022)
- **Amar Patil** (PES1UG24AM031)
- **Chandraraj Patil** (PES1UG24AM425)

---

## Table of Contents
1. [Executive Summary & 2-Minute Elevator Pitch](#1-executive-summary--2-minute-elevator-pitch)
2. [Theoretical Foundations & Behavioral Finance](#2-theoretical-foundations--behavioral-finance)
3. [Data Engineering & Ground Truth Formulation](#3-data-engineering--ground-truth-formulation)
4. [Machine Learning Frameworks Benchmarking](#4-machine-learning-frameworks-benchmarking)
5. [TabNet & Tabular Deep Learning Deep Dive](#5-tabnet--tabular-deep-learning-deep-dive)
6. [Simplicity, Transparency & Efficacy Tri-Dimensional Analysis](#6-simplicity-transparency--efficacy-tri-dimensional-analysis)
7. [Markowitz Modern Portfolio Theory (MPT) Engine](#7-markowitz-modern-portfolio-theory-mpt-engine)
8. [Robo-Advisor Dashboard & Full-Stack Implementation](#8-robo-advisor-dashboard--full-stack-implementation)
9. [Anticipated Examiner Counter-Questions & Model Answers](#9-anticipated-examiner-counter-questions--model-answers)

---

## 1. Executive Summary & 2-Minute Elevator Pitch

### Q: Briefly explain your project and what core problem you are solving.
> **Answer:**  
> Traditional financial advisory and first-generation robo-advisors rely heavily on static **Risk Tolerance Questionnaires (RTQs)**. In behavioral finance, it is well established that human investors suffer from psychological biases: they are overconfident in bull markets and succumb to panic-selling during crashes, misjudging their own risk tolerance. Furthermore, manual questionnaires prevent continuous, automated portfolio rebalancing.  
> 
> In this project, we replace subjective questionnaires with a **supervised machine learning regression framework**. Using the **Federal Reserve Board’s Survey of Consumer Finances (SCF) 2007–2009 panel dataset**, we observe how household balance sheets changed across the 2008 Great Financial Crisis. By filtering for "intelligent investors" whose normalized risk tolerance remained steady ($\le 10\%$ change), we establish an objective, revealed ground truth metric: **True Risk Tolerance**.  
> 
> We benchmark five distinct machine learning frameworks: **XGBoost, Keras Deep MLP, PyTorch with FastAI, PyTorch with TabNet, and PyTorch Lightning**. We evaluate them quantitatively (RMSE, MAE, R², MSE, latency) and qualitatively (Simplicity, Transparency, Efficacy). **XGBoost achieved champion performance ($R^2 = 0.9537$, $\text{RMSE} = 3.46$, latency $= 0.20\text{ ms}$)**. Finally, we embed the calibrated model into a full-stack **Streamlit Robo-Advisor Dashboard** that calculates investor risk tolerance in real-time, solves **Markowitz Mean-Variance Asset Allocation**, and visualizes optimal weights and historical backtest trajectories of a $100 investment.

---

## 2. Theoretical Foundations & Behavioral Finance

### Q: Why do traditional questionnaires fail according to Behavioral Economics?
> **Answer:**  
> 1. **Prospect Theory & Loss Aversion (Kahneman & Tversky, 1979):** The psychological pain of an investment loss is $2\times$ to $2.5\times$ more intense than the pleasure of an equivalent gain. Investors answer surveys assuming rational utility, but act irrationally under real market distress.  
> 2. **Recency & Framing Bias:** When markets are up, investors self-report an aggressive risk tolerance. When markets plummet, fear dominates, causing them to liquidate at market troughs.  
> 3. **Hypothetical Bias:** Answering a multiple-choice question ('What would you do if your portfolio fell 20%?') does not trigger the emotional physiological response of seeing real personal net worth decline.

### Q: What is Wang & Hanna’s (1997) finding regarding Age and Risk Tolerance?
> **Answer:**  
> Contrary to the common folk heuristic that 'older people always take less risk', Wang and Hanna demonstrated that when financial wealth and other socioeconomic variables are controlled for, **relative risk aversion actually decreases as people age** during their peak wealth accumulation years. In our empirical EDA, we observed that middle-aged and older households with substantial accumulated net worth had significantly higher equity risk tolerance than younger, debt-encumbered households.

---

## 3. Data Engineering & Ground Truth Formulation

### Q: Where did you get the dataset and how is it structured?
> **Answer:**  
> We used the **Survey of Consumer Finances (SCF) 2007–2009 Longitudinal Panel Dataset** administered by the Federal Reserve Board. It re-interviewed the same households before the crisis (2007) and after the crash (2009), providing detailed balance sheet items, income, debts, and demographic variables across 4,810 observations.

### Q: How exactly is the target variable 'TrueRiskTol' computed?
> **Answer:**  
> 1. **Asset Categorization:**
>    $$\text{Risky Assets} = \text{Mutual Funds (NMMF)} + \text{Stocks (STOCKS)} + \text{Bonds (BOND)}$$
>    $$\text{Risk-Free Assets} = \text{Checking/Savings (LIQ)} + \text{CDs (CDS)} + \text{Savings Bonds (SAVBND)} + \text{Cash Life Insurance (CASHLI)}$$
> 2. **Pre-Crisis Risk Tolerance (2007):**
>    $$RT_{07} = \frac{\text{Risky}_{07}}{\text{Risky}_{07} + \text{RiskFree}_{07}}$$
> 3. **Market Drawdown Normalization (2009):**
>    Between 2007 and 2009, the S&P 500 index average dropped from **1,478** to **948**. An investor who held the exact same shares would appear to have lower risk tolerance solely because the market price dropped. To isolate behavioral intention:
>    $$RT_{09,\text{norm}} = \left(\frac{\text{Risky}_{09}}{\text{Risky}_{09} + \text{RiskFree}_{09}}\right) \times \left(\frac{948}{1478}\right)$$
> 4. **Intelligent Investor Selection:**
>    An investor who panicked sold equities, causing a sharp drop. An 'intelligent investor' held their allocation constant across the crash:
>    $$\left| \frac{RT_{09,\text{norm}}}{RT_{07}} - 1 \right| \le 0.10 \quad (\le 10\% \text{ change})$$
> 5. **Ground Truth Score:**
>    $$\text{TrueRiskTol} = \left(\frac{RT_{07} + RT_{09,\text{norm}}}{2}\right) \times 100$$
>    Yielding an objective percentage metric scaled between 0 and 100.

### Q: How did you ensure there is NO data leakage?
> **Answer:**  
> **Crucially, all predictor variables are strictly from 2007 (pre-crisis):** `AGE07`, `EDCL07`, `MARRIED07`, `KIDS07`, `OCCAT107`, `INCOME07`, `RISK07`, `NETWORTH07`.  
> The 2009 data was used **only** to establish the historical ground truth target for training. At inference time, the model only requires the investor's current attributes to predict their true risk tolerance.

---

## 4. Machine Learning Frameworks Benchmarking

### Q: Summarize the quantitative results across all 5 frameworks.
> **Answer:**  
> Evaluated on the identical 20% holdout test partition (962 samples):

| Framework | RMSE | MAE | $R^2$ Score | MSE | Train Time | Inference Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **XGBoost (Champion)** | **3.4648** | **1.9063** | **0.9537** | **12.0048** | **0.70 s** | **0.20 ms** |
| **Keras (Deep MLP)** | 7.4283 | 3.8284 | 0.7871 | 55.1804 | 19.22 s | 0.36 ms |
| **PyTorch FastAI** | 8.4073 | 4.5604 | 0.7273 | 70.6820 | 4.81 s | 0.65 ms |
| **PyTorch TabNet** | 9.2111 | 4.5070 | 0.6727 | 84.8450 | 39.51 s | 1.13 ms |
| **PyTorch Lightning** | 8.6479 | 4.2456 | 0.7115 | 74.7857 | 14.31 s | **0.04 ms** |

---

## 5. TabNet & Tabular Deep Learning Deep Dive

### Q: Why did XGBoost outperform TabNet and deep learning neural networks?
> **Answer:**  
> This aligns with the fundamental theoretical and empirical findings of **Grinsztajn, Oyallon, and Varoquaux (NeurIPS 2022)**:
> 1. **Inductive Bias:** Decision tree ensembles split along axis-aligned orthogonal boundaries, which match tabular financial variables (e.g., net worth cutoffs, income brackets) much better than smooth linear combinations used in neural layers.
> 2. **Invariance to Monotonic Transformations:** Tree models are immune to heavy-tailed distributions and extreme monetary outliers without requiring normalization or clipping.
> 3. **Uninformative Features:** Neural networks struggle when some features have high noise or low relevance, whereas gradient boosted trees naturally select the most informative splits.

### Q: What is TabNet and how does its sparse attention mask work?
> **Answer:**  
> TabNet (Arik & Pfister, AAAI 2021) is a deep neural architecture designed specifically for tabular data. It replaces standard dense connections with a **sequential multi-step decision pipeline**:
> - At each step $i$, an **Attentive Transformer** computes a sparse mask $M[i]$ using a `Sparsemax` activation.
> - The mask selects which specific features the network should focus on for that decision step.
> - A **Prior Scale term** prevents the model from relying repeatedly on the same features across all steps.
> - While TabNet provides intrinsic interpretability via these masks, on moderate tabular sample sizes ($N \approx 5,000$), tree boosting remains faster and more accurate.

---

## 6. Simplicity, Transparency & Efficacy Tri-Dimensional Analysis

### Q: How did you define and evaluate Simplicity, Transparency, and Efficacy?
> **Answer:**  
> 1. **Simplicity (Code Brevity & Engineering Overhead):**
>    - **XGBoost (9.2/10):** Scikit-Learn compliant API, zero feature scaling needed, native missing value handling.
>    - **FastAI (8.5/10):** High-level `TabularPandas` automatically handles embeddings and normalization.
>    - **Keras (8.0/10):** Intuitive Sequential API, but requires explicit scaling and callback management.
>    - **Lightning (7.8/10):** Clean separation of concerns, but requires boilerplate DataLoaders and Modules.
>    - **TabNet (7.5/10):** Sensitive hyperparameters (`lambda_sparse`, `n_steps`, virtual batch size).
> 2. **Transparency (Explainability & Regulatory Auditability):**
>    - **XGBoost (9.0/10):** Native feature importance (Gain, Weight, Cover), direct TreeSHAP game-theoretic explainability, and tree path visualization for SEC/FINRA compliance.
>    - **TabNet (8.8/10):** Built-in attention masks show feature importance per decision step.
>    - **FastAI (6.5/10):** Embedding weights are inspectable, but internal dense layers are black-box.
>    - **Lightning (6.2/10) & Keras (6.0/10):** Black-box MLPs requiring external attribution methods.
> 3. **Efficacy (Generalization & Accuracy):**
>    - **XGBoost (9.5/10):** Dominant $R^2 = 0.9537$, lowest error by a wide margin.
>    - **TabNet (8.6/10), FastAI (8.5/10), Lightning (8.3/10), Keras (8.2/10):** Solid non-linear baselines, but prone to variance on skewed financial records.

---

## 7. Markowitz Modern Portfolio Theory (MPT) Engine

### Q: How does the predicted Risk Tolerance link to Markowitz Asset Allocation?
> **Answer:**  
> In Markowitz Modern Portfolio Theory (1952), the investor maximizes quadratic utility:
> $$\max_w \left( w^T \mu - \frac{\lambda}{2} w^T \Sigma w \right)$$
> Subject to:
> $$\sum_{i=1}^N w_i = 1.0 \quad \text{and} \quad 0 \le w_i \le 1.0 \quad (\text{no short selling})$$
> Where:
> - $\mu$ is the expected daily return vector of the selected assets.
> - $\Sigma$ is the covariance matrix of asset returns.
> - $\lambda$ is the **risk aversion coefficient**.
> 
> **Dynamic Calibration:**  
> We dynamically map the predicted continuous True Risk Tolerance ($RT \in [0, 100]$) to $\lambda$:
> $$\lambda(RT) = \frac{100 - RT + 1}{8.5}$$
> - An aggressive investor ($RT = 85$) receives a low penalty ($\lambda \approx 1.88$), causing the optimizer to allocate heavily toward high-return, higher-beta growth equities.
> - A conservative investor ($RT = 15$) receives a heavy penalty ($\lambda \approx 10.12$), forcing the optimizer into low-volatility, defensive assets and cash equivalents.

---

## 8. Robo-Advisor Dashboard & Full-Stack Implementation

### Q: How is the Robo-Advisor Dashboard architected?
> **Answer:**  
> The dashboard is engineered in Python using **Streamlit**, strictly replicating the UI from **Figure 5-6**:
> - **Step 1 (Left Panel):** Sliders for Age, Net Worth, Income, Education, Marital Status, Kids, Occupation, and Survey Risk Willingness. The `CALCULATE RISK TOLERANCE` button triggers inference using the champion XGBoost artifact in 0.20 ms.
> - **Step 2 (Right Panel):** Displays the predicted Risk Tolerance score (scale 0-100), provides a multi-asset selector for S&P 500 stocks (default: GOOGL, META, GS, MS, GE, MSFT), and an optimization trigger.
> - **Visualizations:**
>   1. **Asset Allocation (Bar Chart):** Displays optimal weights derived from the Markowitz SLSQP solver.
>   2. **Historical Performance ($100 Line Chart):** Displays the simulated historical backtest value curve of an initial $100 investment, alongside annualized return, volatility, and Sharpe Ratio.

---

## 9. Anticipated Examiner Counter-Questions & Model Answers

### Q: What if an investor inputs negative Net Worth (e.g. heavy student debt)?
> **Answer:**  
> The model supports negative Net Worth. The training dataset from the SCF includes negative net worth observations (down to -$5.6M). For debt-encumbered individuals, the model predicts low risk tolerance scores ($RT < 3.0$), causing the robo-advisor to allocate conservatively to capital preservation rather than speculative equities.

### Q: Why did you use SLSQP for portfolio optimization instead of analytical matrix inversion?
> **Answer:**  
> Unconstrained Mean-Variance optimization can be solved analytically using Lagrange multipliers, but it routinely produces negative weights (short selling) and extreme leverage. Real retail robo-advisors operate under long-only bounds ($w_i \ge 0$) and full investment constraints ($\sum w_i = 1$). **Sequential Least Squares Programming (SLSQP)** handles these linear equality and inequality constraints efficiently in under 5 milliseconds.

### Q: What are the main limitations of this project and what is the future scope?
> **Answer:**  
> **Current Limitations:**
> 1. Portfolio optimization uses historical returns as proxies for expected returns, which are prone to estimation error.
> 2. Static rebalancing does not adapt dynamically to regime shifts (e.g. sudden interest rate spikes).
> 
> **Future Scope & Next Steps:**
> 1. **Deep Reinforcement Learning (DQN/PPO):** Train autonomous agents for dynamic continuous rebalancing.
> 2. **Black-Litterman Allocation:** Combine CAPM market equilibrium with subjective/macroeconomic views to produce stabilized weight vectors.
> 3. **Automated Tax-Loss Harvesting:** Algorithmically harvest capital losses during downturns to offset investor tax liabilities.
> 4. **Microservices Deployment:** Wrap the engine into a FastAPI backend with Docker and PostgreSQL.

