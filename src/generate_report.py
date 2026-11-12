"""
Machine Learning for Big Data (MLBD) Project Report Generator
Unique, Modern & Elegant 5-Section Report:
  1. Introduction
  2. Methodology
  3. EDA (Exploratory Data Analysis)
  4. Results (Quantitative Table + Simplicity/Transparency/Efficacy Breakdown + Figures)
  5. Conclusion/Summary

Authors:
  - Ananthakrishna M A (PES1UG24AM036)
  - Akash G K (PES1UG24AM022)
  - Amar Patil (PES1UG24AM031)
  - Chandraraj Patil (PES1UG24AM425)

Department of Computer Science & Engineering (AI & ML), PES University
"""

import os
import win32com.client
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
DOCX_OUT = os.path.join(REPORTS_DIR, "MLBD_Project_Report.docx")
PDF_OUT = os.path.join(REPORTS_DIR, "MLBD_Project_Report.pdf")

# Palette
COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB
COLOR_SLATE = RGBColor(71, 85, 105)      # #475569
COLOR_DARK = RGBColor(15, 23, 42)        # #0F172A
COLOR_LIGHT_BG = "F1F5F9"                # #F1F5F9
COLOR_NAVY_HEX = "1E3A8A"
COLOR_ALT_ROW = "F8FAFC"
COLOR_BORDER = "CBD5E1"

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_table_borders(table, border_color=COLOR_BORDER):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="KEY INSIGHT"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, "EFF6FF") # light blue
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only (accent line)
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = COLOR_BLUE
    
    r_txt = p.add_run(text)
    r_txt.font.name = "Arial"
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = COLOR_DARK
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_BLUE
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(11)
    r.bold = True
    r.font.color.rgb = COLOR_SLATE
    return p

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_DARK
        
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_DARK
    return p

def add_bullet_item(doc, text, bold_title=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_title:
        r_b = p.add_run(bold_title)
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(11)
        r_b.bold = True
        r_b.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_DARK
    return p

def add_figure(doc, img_rel_path, caption, width=Inches(6.0)):
    full_path = os.path.join(BASE_DIR, img_rel_path)
    if os.path.exists(full_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(full_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Arial"
        r_cap.font.size = Pt(9.5)
        r_cap.italic = True
        r_cap.font.color.rgb = COLOR_SLATE

def build_unique_report():
    doc = Document()
    
    # Page Setup (A4, 0.8 inch / 2 cm margins)
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("MLBD Mini Project | AI-Driven Investor Risk Tolerance & Robo-Advisor")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_SLATE
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("PES University — Department of Computer Science & Engineering (AI & ML)")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_SLATE

    # ==================== PROJECT TITLE HEADER BLOCK ====================
    title_tbl = doc.add_table(rows=1, cols=1)
    title_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    title_tbl.autofit = False
    title_tbl.columns[0].width = Inches(6.55)
    
    cell_top = title_tbl.rows[0].cells[0]
    set_cell_background(cell_top, "1E3A8A")
    set_cell_margins(cell_top, top=200, bottom=200, left=240, right=240)
    
    p_t1 = cell_top.paragraphs[0]
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_t1.add_run("MACHINE LEARNING FOR BIG DATA (MLBD) — MINI PROJECT REPORT\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.bold = True
    r_sub.font.color.rgb = RGBColor(191, 219, 254) # light blue
    
    r_main = p_t1.add_run("AI-Powered Investor Risk Tolerance Modeling\n& Robo-Advisor Asset Allocation\n")
    r_main.font.name = "Arial"
    r_main.font.size = Pt(17)
    r_main.bold = True
    r_main.font.color.rgb = RGBColor(255, 255, 255)
    
    r_desc = p_t1.add_run("Comparative Benchmarking of XGBoost vs Deep Learning Architectures (Keras, FastAI, TabNet, Lightning) on Survey of Consumer Finances Data")
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(10.5)
    r_desc.font.color.rgb = RGBColor(226, 232, 240)
    
    # Team & Meta Info Table
    meta_tbl = doc.add_table(rows=2, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    meta_tbl.columns[0].width = Inches(3.27)
    meta_tbl.columns[1].width = Inches(3.28)
    set_table_borders(meta_tbl)
    
    c00 = meta_tbl.rows[0].cells[0]
    set_cell_background(c00, "F8FAFC")
    set_cell_margins(c00, top=100, bottom=80, left=140, right=140)
    p_m1 = c00.paragraphs[0]
    p_m1.paragraph_format.line_spacing = 1.15
    r = p_m1.add_run("Student Project Team:\n")
    r.bold = True
    r.font.name = "Arial"
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_NAVY
    
    team_members = [
        ("Ananthakrishna M A", "PES1UG24AM036"),
        ("Akash G K", "PES1UG24AM022"),
        ("Amar Patil", "PES1UG24AM031"),
        ("Chandraraj Patil", "PES1UG24AM425")
    ]
    for name, srn in team_members:
        r_item = p_m1.add_run(f"• {name} ({srn})\n")
        r_item.font.name = "Calibri"
        r_item.font.size = Pt(9.5)
        
    c01 = meta_tbl.rows[0].cells[1]
    set_cell_background(c01, "F8FAFC")
    set_cell_margins(c01, top=100, bottom=80, left=140, right=140)
    p_m2 = c01.paragraphs[0]
    p_m2.paragraph_format.line_spacing = 1.15
    r2 = p_m2.add_run("Academic & Institutional Details:\n")
    r2.bold = True
    r2.font.name = "Arial"
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = COLOR_NAVY
    
    details = [
        ("Course", "Machine Learning for Big Data (MLBD)"),
        ("Department", "Dept. of CSE (AI & ML)"),
        ("Institution", "PES University, Bengaluru"),
        ("Dataset", "Federal Reserve SCF (2007–2009)"),
        ("Repository", "github.com/anantha-bit/Investor-Risk-Tolerance-RoboAdvisor")
    ]
    for k, v in details:
        r_det = p_m2.add_run(f"• {k}: {v}\n")
        r_det.font.name = "Calibri"
        r_det.font.size = Pt(9.5)

    # Empty spacer paragraph
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Executive Summary Card
    add_callout(
        doc,
        "Executive Summary: Traditional wealth advisory evaluates investor risk tolerance through static psychometric questionnaires. These questionnaires fail catastrophically during market drawdowns due to severe cognitive distortions, including hypothetical bias and emotional panic. This project formulates a data-driven paradigm by mining actual household portfolio decisions across the 2007–2009 Global Financial Crisis from the Federal Reserve Survey of Consumer Finances (SCF). We benchmark 5 state-of-the-art machine learning and deep tabular architectures (XGBoost, Keras MLP, PyTorch FastAI, PyTorch TabNet, PyTorch Lightning Flash) across both quantitative accuracy (RMSE, R², MAE) and qualitative dimensions (Simplicity, Transparency, Efficacy). XGBoost achieves top performance (R² = 0.9537, RMSE = 3.4648, Latency = 0.20 ms) and is integrated into an automated Markowitz Mean-Variance portfolio optimization engine deployed via an interactive Streamlit Robo-Advisor dashboard.",
        title="PROJECT ABSTRACT"
    )

    # ==================== 1. INTRODUCTION ====================
    add_heading_1(doc, "1. Introduction")
    
    add_body_p(
        doc,
        "Modern wealth management is fundamentally anchored on the principle of investor risk tolerance—the willingness and financial capacity of an individual to endure fluctuations in the economic value of their investment portfolio. In traditional financial planning, an advisor determines this tolerance by administering a multiple-choice psychometric questionnaire. However, behavioral finance research and empirical evidence from major market crashes reveal that static questionnaires are deeply flawed instruments. When market conditions are favorable, investors systematically overstate their risk appetite (hypothetical bias). Conversely, during systemic crashes, panic selling and recency bias drive investors to liquidate equities at market bottoms, exposing an immense divergence between stated risk attitude and revealed financial action."
    )
    
    add_body_p(
        doc,
        "The emergence of Machine Learning for Big Data provides an unprecedented opportunity to replace flawed heuristic questionnaires with predictive models trained on revealed economic behavior. By analyzing microdata from households that navigated the 2007–2009 Global Financial Crisis, machine learning algorithms can uncover the intricate non-linear relationships linking an investor's demographic profile (age, education, dependents) and balance-sheet capacity (net worth, income, debt obligations, liquid cash) to their actual portfolio allocation decisions."
    )
    
    add_heading_2(doc, "1.1 Problem Statement & Research Motivation")
    add_body_p(
        doc,
        "Wealth advisory platforms and automated robo-advisors face two critical bottlenecks:",
        bold_prefix="Core Problem: "
    )
    add_bullet_item(doc, "Questionnaires evaluate hypothetical sentiment rather than financial capacity, creating severe advisor-client misalignment during market downturns.", bold_title="Cognitive Distortion in Heuristic Profiling: ")
    add_bullet_item(doc, "Deep neural networks are frequently promoted for tabular data, yet systematic benchmarking against gradient-boosted decision trees (GBDT) on empirical financial microdata remains sparse and often lacks rigorous qualitative evaluation.", bold_title="Framework Selection Dilemma: ")
    add_bullet_item(doc, "Financial models must provide auditable, explainable risk estimates to comply with regulatory standards (e.g., FINRA Rule 2111 and SEC Regulation Best Interest).", bold_title="Explainability & Regulatory Scrutiny: ")

    add_heading_2(doc, "1.2 Project Scope & Primary Objectives")
    add_body_p(doc, "To resolve these challenges, this project delivers an end-to-end financial data science solution:")
    add_bullet_item(doc, "Process the Federal Reserve Survey of Consumer Finances (SCF) 2007–2009 Panel dataset, segregating household assets into Risky vs. Risk-Free categories and normalizing for crisis equity deflation.", bold_title="Objective 1 — Data Pipeline: ")
    add_bullet_item(doc, "Implement and train 5 distinct machine learning and deep learning tabular frameworks: XGBoost, Keras Neural Network, PyTorch FastAI, PyTorch TabNet, and PyTorch Lightning Flash.", bold_title="Objective 2 — Multi-Framework Benchmarking: ")
    add_bullet_item(doc, "Conduct a rigorous comparative evaluation across quantitative performance metrics (RMSE, R², MAE, MSE, training duration, inference latency) and tri-dimensional qualitative criteria: Simplicity, Transparency, and Efficacy.", bold_title="Objective 3 — Multi-Dimensional Evaluation: ")
    add_bullet_item(doc, "Mathematically couple the optimal risk prediction model with a Markowitz Mean-Variance Portfolio Optimization engine to calculate dynamically customized asset allocations across equities, bonds, real estate, and cash.", bold_title="Objective 4 — Robo-Advisor Asset Allocation: ")
    add_bullet_item(doc, "Deliver an interactive, enterprise-grade Streamlit web application enabling real-time risk profiling and backtested historical portfolio wealth simulation.", bold_title="Objective 5 — Deployment: ")

    # ==================== 2. METHODOLOGY ====================
    add_heading_1(doc, "2. Methodology")
    
    add_heading_2(doc, "2.1 Dataset Acquisition & Data Pipeline")
    add_body_p(
        doc,
        "The primary data source for this study is the Survey of Consumer Finances (SCF) 2007–2009 Longitudinal Panel, administered by the Federal Reserve Board in cooperation with the Department of the Treasury. Unlike standard cross-sectional surveys, the 2007–2009 panel surveyed the exact same 4,810 households in 2007 (pre-crisis market peak) and re-interviewed them in 2009 (post-crisis market trough). This provides a rare, high-fidelity empirical record of household financial reactions under severe macroeconomic stress."
    )
    
    add_heading_2(doc, "2.2 Asset Segregation & Market Crisis Normalization")
    add_body_p(
        doc,
        "For each surveyed household, total assets are systematically segregated into two mutually exclusive economic categories:"
    )
    add_bullet_item(doc, "Publicly traded equity stocks, stock mutual funds, private business equity interests, and high-yield corporate bonds.", bold_title="Risky Assets: ")
    add_bullet_item(doc, "Checking accounts, savings accounts, money market deposit accounts, certificates of deposit (CDs), U.S. Treasury bills and savings bonds, and cash equivalents.", bold_title="Risk-Free Assets: ")
    
    add_body_p(
        doc,
        "The baseline revealed risk tolerance is defined as the proportion of total wealth allocated to risky instruments: RT = Risky Assets / (Risky Assets + Risk-Free Assets). However, between October 2007 and February 2009, the S&P 500 equity index collapsed from 1,478.49 to 948.33 points (a 35.86% drop, yielding a price deflator scalar s = 948.33 / 1478.49 = 0.6414). If an investor took no action, their 2009 risky asset value would mechanically decline purely from market depreciation. To isolate conscious human asset reallocation from passive market crashes, the 2007 risky asset valuations were normalized to 2009 price levels:",
        bold_prefix="Market Price Normalization: "
    )
    
    add_callout(
        doc,
        "Risky Assets (2007, Normalized) = Risky Assets (2007) * (948.33 / 1,478.49)\n"
        "RT (2007, Normalized) = Risky Assets (2007, Normalized) / [Risky Assets (2007, Normalized) + Risk-Free Assets (2007)]\n"
        "Intelligent Investor Selection Rule: |RT (2009) - RT (2007, Normalized)| <= 0.10\n"
        "Target Ground Truth (TrueRiskTol) = RT (2009) * 100",
        title="MATHEMATICAL FORMULATION"
    )
    
    add_body_p(
        doc,
        "By enforcing the Intelligent Investor criterion (|ΔRT| <= 10%), households that completely panic-sold or made irrational speculative bets are filtered out, yielding 2,610 consistent, financially rational household balance sheets suitable for supervised learning."
    )

    add_heading_2(doc, "2.3 Feature Matrix Engineering")
    add_body_p(doc, "Ten key demographic, financial, and behavioral predictor variables were selected and engineered:")
    
    # Feature Table
    feat_tbl = doc.add_table(rows=11, cols=4)
    feat_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_tbl.autofit = False
    set_table_borders(feat_tbl)
    widths = [Inches(1.2), Inches(1.3), Inches(1.1), Inches(2.9)]
    
    headers = ["Feature", "Category", "Data Type", "Financial & Economic Description"]
    for i, w in enumerate(widths):
        feat_tbl.columns[i].width = w
        c = feat_tbl.rows[0].cells[i]
        set_cell_background(c, COLOR_NAVY_HEX)
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(headers[i])
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    features_info = [
        ("AGE", "Demographic", "Continuous", "Age of the primary household economic respondent"),
        ("EDCL", "Demographic", "Categorical (1-4)", "Education category (1: No HS, 2: HS, 3: College, 4: Degree)"),
        ("MARRIED", "Demographic", "Binary (1/2)", "Marital status (1: Married/Partnered, 2: Unmarried/Single)"),
        ("KIDS", "Demographic", "Integer", "Number of financially dependent children in household"),
        ("NETWORTH", "Financial", "Continuous ($)", "Total household net worth (Assets minus Total Liabilities)"),
        ("INCOME", "Financial", "Continuous ($)", "Annual total household income from wages, capital & transfers"),
        ("LIQ", "Financial", "Continuous ($)", "Total liquid assets immediately available without penalty"),
        ("DEBT", "Financial", "Continuous ($)", "Total household debt liabilities (mortgages, loans, cards)"),
        ("DEBTRATIO", "Financial", "Ratio", "Total household debt obligations divided by annual income"),
        ("RISK_SCALE", "Attitudinal", "Ordinal (1-4)", "Self-reported willingness to take risk from survey question")
    ]
    
    for row_idx, row_data in enumerate(features_info, start=1):
        bg = COLOR_ALT_ROW if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(row_data):
            c = feat_tbl.rows[row_idx].cells[col_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(9)
            if col_idx == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_heading_2(doc, "2.4 Machine Learning & Deep Learning Architectures")
    add_body_p(doc, "To comprehensively compare contemporary paradigms for tabular financial data, five distinct modeling frameworks were engineered:")
    
    add_bullet_item(doc, "Implementation utilizing 300 gradient-boosted decision trees, max tree depth 5, learning rate η = 0.05, subsample ratio 0.8, and histogram-based splitting (tree_method='hist'). Employs second-order Taylor expansion of the loss function and L1/L2 leaf regularization.", bold_title="1. XGBoost (Extreme Gradient Boosted Trees): ")
    add_bullet_item(doc, "Deep Multi-Layer Perceptron (MLP) consisting of Dense layers [64, 32, 16], Batch Normalization layers to prevent internal covariate shift, Dropout regularization (p = 0.20), ReLU activations, and Adam optimizer (learning rate = 0.001, MSE loss).", bold_title="2. Keras Neural Network (PyTorch Backend): ")
    add_bullet_item(doc, "Deep learning tabular learner featuring automated entity embedding layers for discrete categorical variables, continuous batch normalization, weight decay 0.01, and Leslie Smith's One-Cycle learning rate policy for accelerated convergence.", bold_title="3. PyTorch FastAI (TabularLearner): ")
    add_bullet_item(doc, "Canonical attentive tabular neural network featuring sequential decision steps (N_steps = 3, N_d = N_a = 16) with Sparsemax attention transformers. Enforces sparse feature selection per decision step without requiring external feature preprocessing.", bold_title="4. PyTorch TabNet: ")
    add_bullet_item(doc, "Production-grade, modular deep learning architecture with explicit training/validation hooks, gradient clipping (norm 1.0), Early Stopping callbacks (patience = 10), and unified tensor logging.", bold_title="5. PyTorch Lightning Flash: ")

    add_heading_2(doc, "2.5 Markowitz Mean-Variance Asset Allocation Engine")
    add_body_p(
        doc,
        "To operationalize the predicted risk tolerance score (TrueRiskTol ∈ [0, 100]) into an actionable investment portfolio, we couple the model with Modern Portfolio Theory (MPT). The optimal portfolio weight vector w* is obtained by solving the constrained quadratic program:",
        bold_prefix="Optimization Model: "
    )
    
    add_callout(
        doc,
        "Maximize: U(w) = w^T * μ - [λ(TrueRiskTol) / 2] * w^T * Σ * w\n"
        "Subject to: Σ w_i = 1  and  w_i >= 0 (Long-Only, No Leverage)\n\n"
        "Where:\n"
        "• μ is the historical annualized expected return vector across asset classes\n"
        "• Σ is the annual covariance matrix of asset returns\n"
        "• λ(TrueRiskTol) = (100 - TrueRiskTol + 1) / 8.5 is the dynamic risk aversion coefficient",
        title="QUADRATIC UTILITY FORMULATION"
    )
    
    add_body_p(
        doc,
        "Under this calibrated mapping, an aggressive investor (TrueRiskTol = 95) obtains a low risk-aversion coefficient (λ = 0.71), producing high equity weights (SPY ~ 75-85%). Conversely, a conservative investor (TrueRiskTol = 15) obtains a high risk-aversion coefficient (λ = 10.1), driving the optimizer to concentrate capital in risk-free U.S. Treasuries and cash equivalents."
    )

    # ==================== 3. EXPLORATORY DATA ANALYSIS ====================
    add_heading_1(doc, "3. Exploratory Data Analysis (EDA)")
    
    add_heading_2(doc, "3.1 Target Variable Distribution (`TrueRiskTol`)")
    add_body_p(
        doc,
        "Analysis of the crisis-revealed risk tolerance target reveals a distinctly positively skewed, bimodal distribution. A large cluster of households maintains conservative allocations (0% to 20% in risky assets), representing risk-averse individuals who preserve liquid cash reserves. A second, broader cluster appears between 45% and 75%, representing households with substantial stock investments. The overall dataset exhibits a mean risk tolerance of 32.41%, median of 26.50%, and standard deviation of 24.82%."
    )
    
    add_figure(doc, "visualizations/eda_01_target_distribution.png", "Figure 1: Statistical Distribution of Revealed Risk Tolerance (TrueRiskTol) in the Processed SCF Cohort")

    add_heading_2(doc, "3.2 Correlation Heatmap & Financial Drivers")
    add_body_p(
        doc,
        "Pairwise Pearson correlation analysis reveals significant structural relationships across household balance sheets and demographic attributes:"
    )
    add_bullet_item(doc, "Net Worth (r = +0.48) and Liquid Assets (r = +0.42) display the strongest positive correlations with risk tolerance, confirming that financial capacity is the primary prerequisite for equity exposure.", bold_title="Wealth & Liquidity Dominance: ")
    add_bullet_item(doc, "Age exhibits a consistent negative correlation (r = -0.26) with risk tolerance, in strong alignment with the financial lifecycle hypothesis: younger households have longer investment horizons to recover from equity drawdowns.", bold_title="Age & Lifecycle Decline: ")
    add_bullet_item(doc, "Education level correlates positively with risk tolerance (r = +0.31), reflecting financial literacy and higher career income trajectories.", bold_title="Educational Endowment: ")
    
    add_figure(doc, "visualizations/eda_02_correlation_heatmap.png", "Figure 2: Correlation Heatmap Across Demographic, Balance-Sheet, and Risk Variables")

    add_heading_2(doc, "3.3 The Behavioral Gap: Subjective vs. Revealed Risk Tolerance")
    add_body_p(
        doc,
        "A critical empirical discovery of this study is the dramatic divergence between self-reported willingness to take risk (RISK_SCALE) and actual crisis behavior. When cross-analyzing survey responses against balance sheets, households who categorized themselves as willing to take 'substantial financial risk' frequently held less than 30% of their net worth in risky assets during the crash. The correlation between stated risk willingness and actual allocation is a meager r = 0.184."
    )
    
    add_figure(doc, "visualizations/eda_05_subjective_vs_revealed_risk.png", "Figure 3: Behavioral Divergence — Self-Reported Risk Scale vs. Actual Crisis-Revealed Allocation")

    add_heading_2(doc, "3.4 Demographics & Financial Capacity Dynamics")
    add_body_p(
        doc,
        "Disaggregating risk tolerance across net worth brackets and age groups demonstrates non-linear step-changes. Households in the top net worth quartile maintain average risk tolerances exceeding 55%, compared to under 12% for the bottom quartile. Furthermore, married households exhibit higher financial stability and risk capacity than single households with dependents."
    )
    
    add_figure(doc, "visualizations/eda_03_demographics_vs_risk.png", "Figure 4: Risk Tolerance Distributions Segmented by Demographic Categories (Age, Education, Marital Status)")

    # ==================== 4. RESULTS ====================
    add_heading_1(doc, "4. Results & Comparative Evaluation")
    
    add_heading_2(doc, "4.1 Quantitative Performance Benchmarking")
    add_body_p(
        doc,
        "All five architectures were evaluated on an identical held-out test dataset (20% split, N = 522 households). Comprehensive quantitative metrics—including Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), Coefficient of Determination (R²), Mean Squared Error (MSE), Training Duration (seconds), and Inference Latency (milliseconds per sample)—are summarized in Table 2."
    )
    
    # Quantitative Benchmark Table
    bench_tbl = doc.add_table(rows=6, cols=7)
    bench_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    bench_tbl.autofit = False
    set_table_borders(bench_tbl)
    
    col_w = [Inches(1.2), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.95), Inches(0.95), Inches(0.9)]
    for i, w in enumerate(col_w):
        bench_tbl.columns[i].width = w
        c = bench_tbl.rows[0].cells[i]
        set_cell_background(c, COLOR_NAVY_HEX)
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        headers_q = ["Model", "RMSE", "MAE", "R² Score", "MSE", "Train Time", "Latency"]
        r = p.add_run(headers_q[i])
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    benchmark_data = [
        ("XGBoost", "3.4648", "1.9063", "0.9537", "12.0048", "0.70 s", "0.20 ms"),
        ("Keras MLP", "7.4283", "3.8284", "0.7871", "55.1804", "19.22 s", "0.36 ms"),
        ("PyTorch FastAI", "8.4073", "4.5604", "0.7273", "70.6820", "4.81 s", "0.65 ms"),
        ("PyTorch Lightning", "8.6479", "4.2456", "0.7115", "74.7857", "14.31 s", "0.04 ms"),
        ("PyTorch TabNet", "9.2111", "4.5070", "0.6727", "84.8450", "39.51 s", "1.13 ms")
    ]
    
    for row_idx, rdata in enumerate(benchmark_data, start=1):
        bg = "ECFDF5" if row_idx == 1 else (COLOR_ALT_ROW if row_idx % 2 == 1 else "FFFFFF")
        for cidx, val in enumerate(rdata):
            c = bench_tbl.rows[row_idx].cells[cidx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if cidx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            if row_idx == 1 or cidx == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_body_p(
        doc,
        "As demonstrated by Table 2, XGBoost achieved extraordinary predictive superiority over all four deep neural network architectures. XGBoost attained an R² score of 0.9537 and an RMSE of 3.4648 percentage points—reducing predictive error by more than 53% compared to the strongest deep learning alternative (Keras MLP with R² = 0.7871). In addition, XGBoost required only 0.70 seconds of training time and delivered ultra-low inference latency of 0.20 ms per investor profile."
    )
    
    add_figure(doc, "visualizations/model_metrics_comparison.png", "Figure 5: Comparative Evaluation of RMSE, MAE, R², and MSE Across the 5 Modeling Frameworks")

    add_heading_2(doc, "4.2 Qualitative Tri-Dimensional Comparison: Simplicity, Transparency, Efficacy")
    add_body_p(
        doc,
        "In enterprise financial environments, algorithmic performance cannot be judged purely on loss metrics. Fiduciary duty and compliance mandates require evaluating models across three qualitative dimensions:"
    )
    add_bullet_item(doc, "Implementation complexity, hyperparameter sensitivity, boilerplate overhead, and ease of production deployment.", bold_title="1. Simplicity: ")
    add_bullet_item(doc, "Model interpretability, availability of native feature attributions, and capability to audit decisions for regulatory compliance (FINRA/SEC).", bold_title="2. Transparency: ")
    add_bullet_item(doc, "Generalization fidelity on tabular data, robustness against multicollinearity and skewed distributions, and predictive power.", bold_title="3. Efficacy: ")
    
    # Qualitative Breakdown Table
    qual_tbl = doc.add_table(rows=6, cols=4)
    qual_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    qual_tbl.autofit = False
    set_table_borders(qual_tbl)
    
    q_widths = [Inches(1.2), Inches(1.75), Inches(1.8), Inches(1.75)]
    for i, w in enumerate(q_widths):
        qual_tbl.columns[i].width = w
        c = qual_tbl.rows[0].cells[i]
        set_cell_background(c, COLOR_NAVY_HEX)
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        headers_dim = ["Framework", "Simplicity (Implementation)", "Transparency (Interpretability)", "Efficacy (Tabular Accuracy)"]
        r = p.add_run(headers_dim[i])
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    qual_data = [
        ("XGBoost\n(Score: 9.2 / 9.0 / 9.5)",
         "Minimal code boilerplate; native missing-value imputation; handles unscaled numeric variables seamlessly.",
         "High transparency; built-in Gain/Cover metrics; full TreeSHAP compatibility for exact local explanations.",
         "Outstanding efficacy (R² = 0.9537); robust to extreme financial outliers and tabular skewness."),
        ("Keras MLP\n(Score: 8.0 / 6.0 / 8.2)",
         "High-level Sequential API is intuitive; requires manual MinMax scaling and explicit validation callbacks.",
         "Low transparency (black-box); requires slow perturbation methods (KernelSHAP) for post-hoc interpretation.",
         "Good non-linear modeling (R² = 0.7871); sensitive to learning rates and batch normalization placement."),
        ("PyTorch FastAI\n(Score: 8.5 / 6.5 / 8.5)",
         "TabularPandas automates categorical embedding dimensions; One-Cycle policy accelerates learning.",
         "Moderate; categorical embedding clusters can be visualized, but dense layers remain opaque.",
         "Competitive baseline (R² = 0.7273); strong representation learning for discrete demographic attributes."),
        ("PyTorch TabNet\n(Score: 7.5 / 8.8 / 8.6)",
         "High parameter sensitivity (lambda_sparse, n_steps); slowest training duration (39.51 seconds).",
         "High transparency; sequential sparse attention masks reveal exact feature selections per decision step.",
         "Moderate tabular performance (R² = 0.6727); prone to underfitting on moderate sample sizes (N ~ 2,600)."),
        ("PyTorch Lightning\n(Score: 7.8 / 6.2 / 8.3)",
         "Structured object-oriented engineering; high boilerplate overhead for single tabular workflows.",
         "Low; standard deep neural network opacity; requires third-party interpretability libraries.",
         "Solid generalization (R² = 0.7115); hardware-agnostic training loop and clean gradient management.")
    ]
    
    for row_idx, rdata in enumerate(qual_data, start=1):
        bg = "ECFDF5" if row_idx == 1 else (COLOR_ALT_ROW if row_idx % 2 == 1 else "FFFFFF")
        for cidx, val in enumerate(rdata):
            c = qual_tbl.rows[row_idx].cells[cidx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if cidx == 0:
                r.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_figure(doc, "visualizations/model_radar_evaluation.png", "Figure 6: Multi-Dimensional Radar Evaluation: Simplicity, Transparency, and Efficacy Across the 5 Architectures")

    add_heading_2(doc, "4.3 Feature Importance & Economic Attribution")
    add_body_p(
        doc,
        "Inspection of the top-performing XGBoost model's feature gain scores highlights the dominant economic determinants of revealed risk tolerance. Net Worth is the single most critical predictor (38.4% total gain), followed by Liquid Assets (24.1%), Age (14.2%), and Total Income (11.5%). Subjective risk scale accounts for merely 5.7% of model gain, quantitatively proving that an investor's balance sheet capacity outweighs stated psychological willingness."
    )
    
    add_figure(doc, "visualizations/feature_importance_xgboost.png", "Figure 7: Feature Importance Gain Distribution for the Top-Performing XGBoost Architecture")

    add_heading_2(doc, "4.4 Model Prediction Fidelity (Actual vs. Predicted)")
    add_body_p(
        doc,
        "Figure 8 illustrates actual versus predicted risk tolerance scores across all five evaluated models. XGBoost tightly hugs the 45-degree ideal regression line across the full risk spectrum. Deep neural networks exhibit noticeable variance inflation and regression towards the mean in extreme conservative (< 10%) and aggressive (> 80%) regions."
    )
    
    add_figure(doc, "visualizations/actual_vs_predicted_all_models.png", "Figure 8: Actual vs. Predicted Risk Tolerance Regressions Across All 5 Modeling Frameworks")

    # ==================== 5. CONCLUSION / SUMMARY ====================
    add_heading_1(doc, "5. Conclusion / Summary")
    
    add_body_p(
        doc,
        "This project successfully designed, implemented, and benchmarked an end-to-end machine learning system for predicting investor risk tolerance and generating automated robo-advisor asset allocations using Federal Reserve Survey of Consumer Finances (SCF) panel data.",
        bold_prefix="Project Summary: "
    )
    
    add_heading_2(doc, "5.1 Key Findings & Scientific Takeaways")
    add_bullet_item(doc, "Gradient-boosted decision trees (XGBoost) heavily outperformed deep learning architectures (Keras, FastAI, TabNet, Lightning Flash) on tabular financial microdata, achieving an R² of 0.9537 compared to 0.67–0.78 for neural approaches. This aligns with modern empirical machine learning literature confirming tree-based inductive bias superiority for tabular data with heterogeneous numerical features.", bold_title="1. Tabular Machine Learning Hegemony: ")
    add_bullet_item(doc, "Traditional risk profiling questionnaires fail to reflect real-world financial behavior. Stated risk willingness exhibits a weak correlation (r = 0.184) with actual crisis actions. Objective balance-sheet capacity (Net Worth, Liquidity, Debt-to-Income) is the true driver of household risk tolerance.", bold_title="2. Demise of Subjective Questionnaires: ")
    add_bullet_item(doc, "XGBoost emerged as the optimal production choice, combining peak predictive efficacy (3.46 RMSE) with high transparency (TreeSHAP auditability) and supreme operational simplicity (0.70 s training, 0.20 ms latency). For scenarios requiring intrinsic deep attention mechanisms, TabNet provides meaningful sequential attention masks.", bold_title="3. Multi-Criteria Framework Selection: ")
    add_bullet_item(doc, "Coupling non-linear machine learning risk predictions with quadratic Markowitz Mean-Variance optimization provides a robust, scientifically rigorous, and individualized asset allocation engine.", bold_title="4. Practical Robo-Advisor Synthesis: ")

    add_heading_2(doc, "5.2 System Implementation & Repository Deliverables")
    add_body_p(
        doc,
        "All components of this project have been fully developed, tested, and pushed to the public GitHub repository at https://github.com/anantha-bit/Investor-Risk-Tolerance-RoboAdvisor:"
    )
    add_bullet_item(doc, "src/preprocess_scf.py (raw data ingestion & crisis normalization) and src/eda.py (automated exploratory analysis generating 6 publication charts).", bold_title="Data Pipeline: ")
    add_bullet_item(doc, "src/train_models.py (end-to-end training and multi-metric benchmarking of XGBoost, Keras, FastAI, TabNet, and Lightning).", bold_title="Model Benchmarking: ")
    add_bullet_item(doc, "src/portfolio_optimization.py (Markowitz SLSQP quadratic solver with dynamic risk aversion mapping).", bold_title="Optimization Engine: ")
    add_bullet_item(doc, "app.py (interactive Streamlit web dashboard replicating commercial robo-advisor workflows with interactive risk profiling, efficient frontier generation, and $100 historical wealth backtesting).", bold_title="Robo-Advisor Dashboard: ")
    add_bullet_item(doc, "Four self-contained, reproducible Jupyter notebooks in notebooks/ covering Data Pipeline, EDA, 5-Model Benchmarking, and Portfolio Optimization.", bold_title="Interactive Notebooks: ")
    add_bullet_item(doc, "VIVA_PREPARATION_GUIDE.md containing comprehensive theoretical, mathematical, and algorithmic viva questions and model answers.", bold_title="Examination Preparation: ")

    # Closing sign-off box
    add_callout(
        doc,
        "Project Status: Fully completed and verified.\n"
        "Repository: https://github.com/anantha-bit/Investor-Risk-Tolerance-RoboAdvisor\n"
        "Authors: Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), Chandraraj Patil (PES1UG24AM425)\n"
        "Department of Computer Science & Engineering (AI & ML), PES University, Bengaluru.",
        title="SUBMISSION VERIFICATION"
    )

    # Save DOCX
    doc.save(DOCX_OUT)
    print(f"[OK] Word document successfully saved to: {DOCX_OUT}")

    # Convert to PDF via Word COM Automation
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(DOCX_OUT)
        doc_com.SaveAs(PDF_OUT, FileFormat=17) # 17 = wdFormatPDF
        doc_com.Close()
        word.Quit()
        print(f"[OK] PDF successfully generated: {PDF_OUT}")
    except Exception as e:
        print(f"[WARN] Could not convert to PDF via COM: {e}")

if __name__ == "__main__":
    build_unique_report()
