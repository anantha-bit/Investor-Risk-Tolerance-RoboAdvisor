"""
Professional PowerPoint Presentation Generator
Creates an academic and executive slide deck for Capstone Project Phase - 1
with clean typography, structured tables, visual callouts, and performance charts.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PPTX_OUT = os.path.join(BASE_DIR, "reports", "Investor_Risk_Tolerance_RoboAdvisor_Presentation.pptx")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

# Palette Constants
COLOR_NAVY = RGBColor(16, 37, 66)       # Primary dark
COLOR_GOLD = RGBColor(212, 175, 55)     # Accent gold
COLOR_BLUE = RGBColor(31, 119, 180)     # Primary brand blue
COLOR_LIGHT_BG = RGBColor(245, 247, 250)# Card background
COLOR_DARK_TEXT = RGBColor(33, 37, 41)  # Charcoal text
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(108, 117, 125)


def add_run_text(p, text):
    r = p.add_run()
    r.text = str(text)
    return r

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen layout (13.33 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    def add_slide_header(slide, title_text, category="UE24AM320A — CAPSTONE PROJECT PHASE - 1"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_GOLD
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Georgia"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_NAVY
        
    def add_card(slide, left, top, width, height, bg_color=COLOR_LIGHT_BG, border_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Elegant Theme)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()
    
    t_box1 = slide1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(5.2))
    tf1 = t_box1.text_frame
    tf1.word_wrap = True
    
    p0 = tf1.paragraphs[0]
    p0.text = "PES UNIVERSITY • FACULTY OF ENGINEERING • DEPT OF CSE (AI & ML)"
    p0.font.name = "Arial"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_GOLD
    p0.space_after = Pt(14)
    
    p1 = tf1.add_paragraph()
    p1.text = "Modeling Investor Risk Tolerance and\nEnabling an ML-Based Robo-Advisor"
    p1.font.name = "Georgia"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE
    p1.space_after = Pt(14)
    
    p2 = tf1.add_paragraph()
    p2.text = "A Supervised Learning Benchmark Across 5 Frameworks & Markowitz Asset Allocation"
    p2.font.name = "Arial"
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(200, 215, 235)
    p2.space_after = Pt(28)
    
    p3 = tf1.add_paragraph()
    p3.text = "Project Id: 7 • Course: UE24AM320A (Capstone Project Phase - 1) • Aug – Dec 2026\n"
    p3.text += "Project Team: Ananthakrishna M A (PES1UG24AM036) | Akash G K (PES1UG24AM022)\n"
    p3.text += "              Amar Patil (PES1UG24AM031)        | Chandraraj Patil (PES1UG24AM425)"
    p3.font.name = "Courier New"
    p3.font.size = Pt(12)
    p3.font.color.rgb = RGBColor(220, 220, 220)

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide2, "The Problem: Failure of Traditional Risk Questionnaires")
    
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb2_left = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf2_l = tb2_left.text_frame
    tf2_l.word_wrap = True
    
    p = tf2_l.paragraphs[0]
    p.text = "Flaws in Current Industry Practice"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)
    
    bullet_items = [
        ("Subjective Psychometrics: ", "Traditional wealth advisors rely on 5-to-10 multiple-choice Risk Tolerance Questionnaires (RTQs)."),
        ("Overconfidence in Bull Markets: ", "Investors routinely overestimate their appetite for risk when markets trend upward."),
        ("Panic-Selling in Crises: ", "During sharp crashes (e.g., 2008 Lehman collapse, 2020 liquidity freeze), stated tolerance evaporates, triggering ruinous capital liquidation."),
        ("Manual Friction: ", "Questionnaires require manual client completion, eliminating the possibility of end-to-end robo-advisory automation.")
    ]
    for b_title, b_text in bullet_items:
        p = tf2_l.add_paragraph()
        p.space_after = Pt(8)
        r1 = add_run_text(p, b_title)
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_NAVY
        r2 = add_run_text(p, b_text)
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_DARK_TEXT

    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), bg_color=COLOR_NAVY)
    tb2_right = slide2.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.8))
    tf2_r = tb2_right.text_frame
    tf2_r.word_wrap = True
    
    p = tf2_r.paragraphs[0]
    p.text = "The Machine Learning Solution"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(14)
    
    sol_items = [
        ("Objective Ground Truth: ", "Extract revealed financial behavior from longitudinal balance sheets across the 2008 Great Financial Crisis."),
        ("Supervised Regression: ", "Map demographic traits, income, and net worth directly to continuous True Risk Tolerance (0 to 100)."),
        ("Markowitz MPT Coupling: ", "Dynamically calibrate quadratic risk aversion λ directly into Modern Portfolio Theory optimization."),
        ("Automated Robo-Advising: ", "Deliver a fully interactive web platform that calculates asset allocation free of human bias.")
    ]
    for s_title, s_text in sol_items:
        p = tf2_r.add_paragraph()
        p.space_after = Pt(10)
        r1 = add_run_text(p, s_title)
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_GOLD
        r2 = add_run_text(p, s_text)
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 3: Federal Reserve SCF Panel Data Pipeline
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide3, "Data Engineering: Federal Reserve SCF 2007-2009 Panel")
    
    # 3 Cards across the slide
    cards_data = [
        ("1. Asset Decomposition", [
            ("Risky Assets (R):", "Equities, non-money market mutual funds, corporate & municipal bonds."),
            ("Risk-Free Assets (RF):", "Checking accounts, CDs, savings bonds, cash life insurance."),
            ("Pre-Crisis Allocation:", "RT_07 = R_07 / (R_07 + RF_07)")
        ], Inches(0.8)),
        ("2. Crisis Normalization", [
            ("Macroeconomic Shock:", "S&P 500 crashed from 1,478 (2007 avg) to 948 (2009 avg)."),
            ("Adjustment Ratio:", "Market ratio = 948 / 1478 = 0.6414."),
            ("Normalized Metric:", "RT_09_norm = [R_09 / (R_09 + RF_09)] × (948 / 1478)")
        ], Inches(4.8)),
        ("3. Intelligent Investor Filter", [
            ("Behavioral Discipline:", "Filter households with allocation change ≤ 10% across crisis:"),
            ("Formula:", "| (RT_09_norm / RT_07) - 1 | ≤ 0.10"),
            ("Ground Truth Target:", "TrueRiskTol = [(RT_07 + RT_09_norm) / 2] × 100 (4,810 records)")
        ], Inches(8.8))
    ]
    for c_title, c_bullets, c_left in cards_data:
        add_card(slide3, c_left, Inches(1.8), Inches(3.7), Inches(5.0))
        tb = slide3.shapes.add_textbox(c_left + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.6))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = c_title
        p.font.name = "Georgia"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(14)
        
        for b_lbl, b_val in c_bullets:
            p = tf.add_paragraph()
            p.space_after = Pt(8)
            r1 = add_run_text(p, b_lbl + "\n")
            r1.font.bold = True
            r1.font.size = Pt(11)
            r1.font.color.rgb = COLOR_BLUE
            r2 = add_run_text(p, b_val)
            r2.font.size = Pt(11)
            r2.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 4: Exploratory Data Analysis & Behavioral Gap
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide4, "Exploratory Data Analysis: Revealing the Behavioral Gap")
    
    # Left: Image
    img_eda = os.path.join(VIZ_DIR, "eda_05_subjective_vs_revealed_risk.png")
    if os.path.exists(img_eda):
        slide4.shapes.add_picture(img_eda, Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.8))
        
    # Right: Narrative Box
    add_card(slide4, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    tb4 = slide4.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.2), Inches(4.4))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "Key Empirical Discoveries"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)
    
    eda_findings = [
        ("Weak Correlation (r = -0.28): ", "Self-reported willingness to take risk only weakly tracks actual equity holdings."),
        ("Survey Overstatement: ", "Respondents claiming 'Substantial Risk' appetite held over 75% in cash and CDs."),
        ("Balance Sheet Primacy: ", "Net worth and income are the overwhelming empirical predictors of equity risk-taking capacity."),
        ("Age Lifecycle Dynamics: ", "Consistent with Wang & Hanna (1997), risk tolerance exhibits an inverted-U lifecycle curve, rising into peak earning years.")
    ]
    for ef_title, ef_body in eda_findings:
        p = tf4.add_paragraph()
        p.space_after = Pt(8)
        r1 = add_run_text(p, ef_title)
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_NAVY
        r2 = add_run_text(p, ef_body)
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 5: 5-Framework Regression Architecture
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide5, "The 5 Machine Learning Frameworks Evaluated")
    
    fw_boxes = [
        ("1. XGBoost", "Gradient Boosted Trees", "350 estimators, max_depth=5, learning_rate=0.04, col/row subsampling=0.85. Native handling of mixed tabular distributions.", Inches(0.8), Inches(1.8)),
        ("2. Keras (PyTorch)", "Deep Multi-Layer Perceptron", "Unified Keras 3 with Torch backend. 128-64-32 architecture, Batch Normalization, Dropout (20%/15%), Adam optimizer with ReduceLROnPlateau.", Inches(4.8), Inches(1.8)),
        ("3. PyTorch FastAI", "Tabular Learner & Embeddings", "Categorical embedding layers for ordinal/nominal features. Leslie Smith's One-Cycle Learning Rate Policy over 10 epochs.", Inches(8.8), Inches(1.8)),
        ("4. PyTorch TabNet", "Attentive Decision Steps", "Sequential self-attentive transformer with sparse masks (lambda_sparse=1e-4, 4 steps). Selects salient features per step.", Inches(2.8), Inches(4.5)),
        ("5. PyTorch Lightning", "Structured Tabular Regressor", "Modular LightningModule encapsulating training/validation hooks, AdamW weight decay, and ReduceLROnPlateau scheduling.", Inches(6.8), Inches(4.5))
    ]
    for title, subtitle, desc, left, top in fw_boxes:
        add_card(slide5, left, top, Inches(3.7), Inches(2.4))
        tb = slide5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), Inches(3.4), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Georgia"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_BLUE
        p_sub.space_after = Pt(6)
        
        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(10)
        p_desc.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 6: Quantitative Results Benchmark (Table & Metrics)
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide6, "Quantitative Benchmark Results on Test Partition (N = 962)")
    
    # Table of benchmark metrics
    table_shape = slide6.shapes.add_table(6, 7, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.0))
    table = table_shape.table
    
    headers = ["Framework", "RMSE ↓", "MAE ↓", "R² Score ↑", "MSE ↓", "Train Time", "Inference Latency"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        
    rows_data = [
        ("XGBoost (Champion)", "3.4648", "1.9063", "0.9537", "12.0048", "0.70 s", "0.20 ms"),
        ("Keras Deep MLP", "7.4283", "3.8284", "0.7871", "55.1804", "19.22 s", "0.36 ms"),
        ("PyTorch FastAI", "8.4073", "4.5604", "0.7273", "70.6820", "4.81 s", "0.65 ms"),
        ("PyTorch TabNet", "9.2111", "4.5070", "0.6727", "84.8450", "39.51 s", "1.13 ms"),
        ("PyTorch Lightning", "8.6479", "4.2456", "0.7115", "74.7857", "14.31 s", "0.04 ms")
    ]
    for r_idx, r_vals in enumerate(rows_data):
        for c_idx, val in enumerate(r_vals):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(11)
            p.alignment = PP_ALIGN.CENTER
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = RGBColor(0, 100, 0)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(235, 247, 235)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_WHITE if r_idx % 2 == 1 else RGBColor(245, 245, 245)

    # Callout card beneath table
    add_card(slide6, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.6), bg_color=COLOR_NAVY)
    tb_c = slide6.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.4))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    p = tf_c.paragraphs[0]
    p.text = "Key Quantitative Findings:"
    p.font.name = "Georgia"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(4)
    
    p2 = tf_c.add_paragraph()
    p2.text = "• XGBoost achieved decisive dominance: R² = 0.9537, cutting RMSE to 3.46 (more than 50% lower than deep models).\n"
    p2.text += "• Lightning achieved the fastest inference (0.04 ms), followed by XGBoost (0.20 ms) and Keras (0.36 ms).\n"
    p2.text += "• TabNet required longest training (39.5s) due to iterative sparse attention masks, achieving R² = 0.6727."
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 7: Tri-Dimensional Qualitative Evaluation
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide7, "Qualitative Comparison: Simplicity, Transparency, Efficacy")
    
    img_radar = os.path.join(VIZ_DIR, "model_radar_evaluation.png")
    if os.path.exists(img_radar):
        slide7.shapes.add_picture(img_radar, Inches(0.8), Inches(1.8), Inches(5.2), Inches(5.0))
        
    add_card(slide7, Inches(6.4), Inches(1.8), Inches(6.1), Inches(5.0))
    tb7 = slide7.shapes.add_textbox(Inches(6.6), Inches(2.0), Inches(5.7), Inches(4.6))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    
    p = tf7.paragraphs[0]
    p.text = "Tri-Dimensional Evaluation Rubric"
    p.font.name = "Georgia"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    
    crit_items = [
        ("Simplicity (Code & Workflow Overhead):", 
         "XGBoost (9.2/10) requires zero scaling pipelines and handles missing data natively. FastAI (8.5/10) automates embeddings. PyTorch Lightning (7.8/10) and TabNet (7.5/10) require extensive class scaffolding and parameter tuning."),
        ("Transparency (Regulatory Interpretability):", 
         "XGBoost (9.0/10) offers native Gini importances, split depths, and exact TreeSHAP compliance. TabNet (8.8/10) features sequential attention masks. Deep networks (Keras 6.0, Lightning 6.2) remain black-box opaque."),
        ("Efficacy (Predictive Generalization):", 
         "XGBoost (9.5/10) decisively outperformed all neural models on tabular finance records, aligning with Grinsztajn et al. (NeurIPS 2022) findings on tree-based tabular supremacy.")
    ]
    for c_title, c_text in crit_items:
        p = tf7.add_paragraph()
        p.space_after = Pt(6)
        r1 = add_run_text(p, c_title + "\n")
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = COLOR_BLUE
        r2 = add_run_text(p, c_text)
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 8: Markowitz Portfolio Optimization Engine
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide8, "Modern Portfolio Theory: Dynamic Risk Aversion Mapping")
    
    add_card(slide8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb8_l = slide8.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True
    
    p = tf8_l.paragraphs[0]
    p.text = "Mathematical Formulation"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)
    
    math_text = [
        ("Quadratic Utility Optimization:", "max_w  [ w^T μ - (λ / 2) w^T Σ w ]\nsubject to:  Σ w_i = 1.0  and  0 ≤ w_i ≤ 1.0"),
        ("Dynamic Risk Aversion Mapping:", "λ(RT) = (100 - RT + 1) / 8.5\n• High RT (e.g. 80) -> Low λ (2.4) -> Aggressive equity weighting\n• Low RT (e.g. 10) -> High λ (10.7) -> Defensive capital preservation"),
        ("Numerical Solver:", "Sequential Least Squares Programming (SLSQP) executes constrained quadratic optimization in < 5 ms.")
    ]
    for m_t, m_b in math_text:
        p = tf8_l.add_paragraph()
        p.space_after = Pt(10)
        r1 = add_run_text(p, m_t + "\n")
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_BLUE
        r2 = add_run_text(p, m_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_TEXT

    add_card(slide8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb8_r = slide8.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True
    
    p = tf8_r.paragraphs[0]
    p.text = "Portfolio Backtest & Telemetry"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)
    
    backtest_bullets = [
        ("Historical Simulation: ", "Continuous daily rebalancing simulation of a $100 baseline investment across S&P 500 equities."),
        ("Performance Metrics: ", "Calculates Annualized Expected Return (μ_ann), Annualized Volatility (σ_ann), and Sharpe Ratio (r_f = 2.0%)."),
        ("Regime Robustness: ", "Dynamically re-weights assets according to cross-asset correlation matrix Σ, dampening idiosyncratic shock drawdowns."),
        ("Empirical Case (RT = 23.64): ", "Allocated GOOGL: 20.8%, MSFT: 79.2%, yielding +51.5% total return over the 2-year testing window.")
    ]
    for bt_t, bt_b in backtest_bullets:
        p = tf8_r.add_paragraph()
        p.space_after = Pt(8)
        r1 = add_run_text(p, bt_t)
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_NAVY
        r2 = add_run_text(p, bt_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 9: Interactive Robo-Advisor Dashboard (Figure 5-6 Implementation)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide9, "Robo-Advisor Dashboard (Streamlit Full-Stack UI)")
    
    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb9_l = slide9.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf9_l = tb9_l.text_frame
    tf9_l.word_wrap = True
    
    p = tf9_l.paragraphs[0]
    p.text = "Step 1: Investor Profiling"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    
    s1_items = [
        ("Demographic Inputs: ", "Age slider (20-85), Marital status (1/2), Education level (1-4), Kids count (0-7)."),
        ("Financial Capacity: ", "Net worth slider (-$500k to $5M), Annual income ($10k to $2M)."),
        ("Behavioral Bias: ", "Occupation scale (1-4), Risk willingness survey score (1-4)."),
        ("Action Trigger: ", "'CALCULATE RISK TOLERANCE' button queries champion XGBoost model in 0.20 ms, generating real-time score.")
    ]
    for s_t, s_b in s1_items:
        p = tf9_l.add_paragraph()
        p.space_after = Pt(8)
        r1 = add_run_text(p, s_t)
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_NAVY
        r2 = add_run_text(p, s_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_TEXT

    add_card(slide9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    tb9_r = slide9.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf9_r = tb9_r.text_frame
    tf9_r.word_wrap = True
    
    p = tf9_r.paragraphs[0]
    p.text = "Step 2: Portfolio Optimization"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(10)
    
    s2_items = [
        ("Predicted Score Display: ", "Displays exact predicted True Risk Tolerance score (e.g. 23.64 / 100)."),
        ("Asset Multi-Selector: ", "Allows selecting S&P 500 assets (default: GOOGL, META, GS, MS, GE, MSFT)."),
        ("Mean-Variance Bar Chart: ", "Displays bright red optimal weight bars exactly replicating Figure 5-6."),
        ("Historical Backtest Curve: ", "Plots simulated daily trajectory of a $100 investment, displaying Expected Return, Volatility, and Sharpe Ratio.")
    ]
    for s_t, s_b in s2_items:
        p = tf9_r.add_paragraph()
        p.space_after = Pt(8)
        r1 = add_run_text(p, s_t)
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_NAVY
        r2 = add_run_text(p, s_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_TEXT

    # =========================================================================
    # SLIDE 10: Phase-1 Conclusion & Phase-2 Roadmap
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    add_slide_header(slide10, "Conclusion of Phase - 1 and Phase - 2 Future Roadmap")
    
    add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    tb10_l = slide10.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.6))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True
    
    p = tf10_l.paragraphs[0]
    p.text = "Phase - 1 Milestones Achieved"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(12)
    
    milestones = [
        ("Longitudinal Ground Truth: ", "Extracted and normalized Federal Reserve SCF panel across the 2008 crash."),
        ("Behavioral Bias Discovered: ", "Empirically proved questionnaire subjectivity and wealth capacity dominance."),
        ("5-Framework Rigorous Benchmark: ", "Evaluated XGBoost, Keras, FastAI, TabNet, Lightning on RMSE, MAE, R², latency."),
        ("Champion Model Isolated: ", "XGBoost delivered R² = 0.9537 with 0.20 ms latency."),
        ("Interactive Web Dashboard: ", "Delivered working Streamlit application replicating Figure 5-6.")
    ]
    for m_t, m_b in milestones:
        p = tf10_l.add_paragraph()
        p.space_after = Pt(7)
        r1 = add_run_text(p, m_t)
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_BLUE
        r2 = add_run_text(p, m_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_DARK_TEXT

    add_card(slide10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0), bg_color=COLOR_NAVY)
    tb10_r = slide10.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.6))
    tf10_r = tb10_r.text_frame
    tf10_r.word_wrap = True
    
    p = tf10_r.paragraphs[0]
    p.text = "Phase - 2 Future Work Roadmap"
    p.font.name = "Georgia"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(12)
    
    p2_items = [
        ("1. Deep Reinforcement Learning: ", "Deploy DQN / PPO agents for continuous rebalancing in non-stationary market regimes."),
        ("2. Multi-Asset Class Expansion: ", "Incorporate global commodities, REITs, sovereign debt, and digital assets."),
        ("3. Black-Litterman Bayesian MPT: ", "Blend market equilibrium with investor views to alleviate estimation error sensitivity."),
        ("4. Automated Tax-Loss Harvesting: ", "Algorithmically harvest capital losses during downturns to maximize after-tax alpha."),
        ("5. Cloud Microservices & REST API: ", "Containerize with Docker, FastAPI, and PostgreSQL for live brokerage deployment.")
    ]
    for p_t, p_b in p2_items:
        p = tf10_r.add_paragraph()
        p.space_after = Pt(7)
        r1 = add_run_text(p, p_t)
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = COLOR_GOLD
        r2 = add_run_text(p, p_b)
        r2.font.size = Pt(11)
        r2.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 11: Viva Voce & Thank You
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    bg11 = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg11.fill.solid()
    bg11.fill.fore_color.rgb = COLOR_NAVY
    bg11.line.fill.background()
    
    tb11 = slide11.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.0))
    tf11 = tb11.text_frame
    tf11.word_wrap = True
    
    p = tf11.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Thank You"
    p.font.name = "Georgia"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(16)
    
    p2 = tf11.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Questions & Answers (Viva Voce Defense)"
    p2.font.name = "Arial"
    p2.font.size = Pt(22)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(24)
    
    p3 = tf11.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "GitHub Repository: https://github.com/anantha-bit/Investor-Risk-Tolerance-RoboAdvisor\n"
    p3.text += "Department of Computer Science and Engineering (AI & ML) • PES University"
    p3.font.name = "Courier New"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(200, 215, 235)

    print(f"[PPTX] Saving slide deck to {PPTX_OUT}...")
    prs.save(PPTX_OUT)
    print(f"[OK] Presentation saved successfully ({os.path.getsize(PPTX_OUT):,} bytes)")

if __name__ == "__main__":
    create_deck()
