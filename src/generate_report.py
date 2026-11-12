"""
Academic MLBD Mini Project Report Generator
Complies with PES University Report Guidelines:
- A4 size, 2.0 cm margins on all sides
- 1.5 line spacing, Times New Roman font
- Chapter Title: 18 pt (centered, bold)
- Section Title: 16 pt (bold, left)
- Subsection Title: 14 pt (bold, left)
- Body text: 12 pt (justified)
- All required chapters, tables, figures, citations, and appendix
- Exports to .docx and converts natively to .pdf via Microsoft Word COM automation
"""

import os
import win32com.client
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCX_OUT = os.path.join(BASE_DIR, "reports", "MLBD_Mini_Project_Report.docx")
PDF_OUT = os.path.join(BASE_DIR, "reports", "MLBD_Mini_Project_Report.pdf")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_header_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    run = h.runs[0]
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0, 0, 0)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.line_spacing = 1.5
    if level == 1:
        run.font.size = Pt(18)
        run.bold = True
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        run.font.size = Pt(16)
        run.bold = True
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 3:
        run.font.size = Pt(14)
        run.bold = True
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return h

def add_body_p(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_bullet_p(doc, text, bold_title=None):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    if bold_title:
        r_t = p.add_run(bold_title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(12)
        r_t.bold = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

def add_image_figure(doc, img_path, caption, width=Inches(6.0)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10.5)
        r_cap.font.italic = True
    else:
        print(f"[WARN] Image {img_path} not found.")

def build_report():
    print("[REPORT] Creating document structure...")
    doc = Document()
    
    # Page Setup: A4, 2.0 cm margins (0.7874 inches)
    sections = doc.sections
    for s in sections:
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)
        s.top_margin = Inches(0.7874)
        s.bottom_margin = Inches(0.7874)
        s.left_margin = Inches(0.7874)
        s.right_margin = Inches(0.7874)
        
    # =========================================================================
    # INNER TITLE PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Project Report on\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    
    r_title = p.add_run("“MODELING INVESTOR RISK TOLERANCE AND ENABLING A MACHINE LEARNING–BASED ROBO-ADVISOR”\n\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.bold = True
    
    r_sub = p.add_run("Submitted in partial fulfilment of the requirements for the award of the degree\nof\n")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(12)
    
    r_deg = p.add_run("Bachelor of Technology\nin\nComputer Science and Engineering (AI & ML)\n\n")
    r_deg.font.name = 'Times New Roman'
    r_deg.font.size = Pt(14)
    r_deg.bold = True
    
    r_crs = p.add_run("Machine Learning for Big Data (MLBD) — Mini Project\nPW26_ID07\n\nSubmitted by:\n")
    r_crs.font.name = 'Times New Roman'
    r_crs.font.size = Pt(12)
    
    # Team Table
    table_team = doc.add_table(rows=5, cols=2)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ("Candidate Name", "SRN"),
        ("Ananthakrishna M A", "PES1UG24AM036"),
        ("Akash G K", "PES1UG24AM022"),
        ("Amar Patil", "PES1UG24AM031"),
        ("Chandraraj Patil", "PES1UG24AM425")
    ]
    for r_idx, (name, srn) in enumerate(team_data):
        row = table_team.rows[r_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.text, c1.text = name, srn
        for c in (c0, c1):
            p_c = c.paragraphs[0]
            p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_c.paragraph_format.line_spacing = 1.15
            for run_c in p_c.runs:
                run_c.font.name = 'Times New Roman'
                run_c.font.size = Pt(11)
                if r_idx == 0:
                    run_c.bold = True
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            if r_idx == 0:
                set_cell_background(c, "E8EEF5")
                
    p_guid = doc.add_paragraph()
    p_guid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guid.paragraph_format.space_before = Pt(18)
    p_guid.paragraph_format.line_spacing = 1.25
    r_g = p_guid.add_run("\nUnder the guidance of\nFaculty Guide, Department of CSE (AI & ML)\nPES University, Bengaluru\n\nAugust – December 2026\n\n")
    r_g.font.name = 'Times New Roman'
    r_g.font.size = Pt(12)
    
    r_inst = p_guid.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (AI & ML)\nFACULTY OF ENGINEERING\nPES UNIVERSITY\n")
    r_inst.font.name = 'Times New Roman'
    r_inst.font.size = Pt(13)
    r_inst.bold = True
    
    r_addr = p_guid.add_run("(Established under Karnataka Act No. 16 of 2013)\n100 Feet Ring Road, BSK 3rd Stage, Hosakerehalli, Bengaluru – 560085\n")
    r_addr.font.name = 'Times New Roman'
    r_addr.font.size = Pt(10)
    
    doc.add_page_break()
    
    # =========================================================================
    # CERTIFICATE
    # =========================================================================
    p_cert_hdr = doc.add_paragraph()
    p_cert_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ch = p_cert_hdr.add_run("PES UNIVERSITY\n(Established under Karnataka Act No. 16 of 2013)\n100ft Ring Road, Bengaluru – 560 085, Karnataka, India\nFACULTY OF ENGINEERING\n\nCERTIFICATE\n")
    r_ch.font.name = 'Times New Roman'
    r_ch.font.size = Pt(14)
    r_ch.bold = True
    
    add_body_p(doc, "This is to certify that the project report entitled “Modeling Investor Risk Tolerance and Enabling a Machine Learning–Based Robo-Advisor” is a bonafide work carried out by Ananthakrishna M A (PES1UG24AM036), Akash G K (PES1UG24AM022), Amar Patil (PES1UG24AM031), and Chandraraj Patil (PES1UG24AM425) in partial fulfilment for the completion of Fifth-semester Machine Learning for Big Data (MLBD) Mini Project in the Program of Study — Bachelor of Technology in Computer Science and Engineering (AI & ML) under the rules and regulations of PES University, Bengaluru during the period August – December 2026. It is certified that all corrections/suggestions indicated for internal assessment have been incorporated in the report. The project has been approved as it satisfies the 5th-semester academic requirements prescribed for the MLBD Mini Project.")
    
    p_sigs = doc.add_paragraph()
    p_sigs.paragraph_format.space_before = Pt(40)
    p_sigs.paragraph_format.line_spacing = 1.5
    p_sigs.add_run("_____________________\t\t\t\t_____________________\nFaculty Guide / Course Instructor\t\t\tChairperson, Dept of CSE (AI & ML)\nPES University, Bengaluru\t\t\tPES University, Bengaluru\n\n\n")
    p_sigs.add_run("Name of the Examiners:\t\t\t\tSignatures with Date:\n1. ___________________\t\t\t\t1. ___________________\n2. ___________________\t\t\t\t2. ___________________")
    for r in p_sigs.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    doc.add_page_break()
    
    # =========================================================================
    # DECLARATION & ACKNOWLEDGEMENT
    # =========================================================================
    add_header_styled(doc, "DECLARATION", level=1)
    add_body_p(doc, "We hereby declare that the MLBD Mini Project entitled “Modeling Investor Risk Tolerance and Enabling a Machine Learning–Based Robo-Advisor” has been carried out by us under the guidance of our Faculty Guide, Department of Computer Science and Engineering (AI & ML), and submitted in partial fulfilment of the course requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (AI & ML) of PES University, Bengaluru during the academic semester August – December 2026. The matter embodied in this report has not been submitted to any other university or institution for the award of any degree or diploma.")
    
    # Signature rows
    p_dec_sign = doc.add_paragraph()
    p_dec_sign.paragraph_format.space_before = Pt(20)
    p_dec_sign.paragraph_format.line_spacing = 1.3
    p_dec_sign.add_run("SRN\t\t\tName\t\t\t\tSignature\n")
    p_dec_sign.add_run("PES1UG24AM036\tAnanthakrishna M A\t\t_____________________\n")
    p_dec_sign.add_run("PES1UG24AM022\tAkash G K\t\t\t_____________________\n")
    p_dec_sign.add_run("PES1UG24AM031\tAmar Patil\t\t\t_____________________\n")
    p_dec_sign.add_run("PES1UG24AM425\tChandraraj Patil\t\t_____________________\n")
    for r in p_dec_sign.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    add_header_styled(doc, "ACKNOWLEDGEMENT", level=1)
    add_body_p(doc, "We express our sincere gratitude to our Faculty Guide and Course Instructors, Department of Computer Science and Engineering (AI & ML), PES University, for valuable mentorship, constructive critiques, and consistent encouragement throughout the conception, empirical analysis, and engineering execution of the MLBD Mini Project.")
    add_body_p(doc, "We extend our gratitude to the Course Coordinators for organizing and systematically guiding the project evaluation phases. We also take this opportunity to thank Dr. Jayashree R, Professor & Chairperson, Department of Computer Science and Engineering (AI & ML), for providing world-class infrastructure and departmental resources. We also thank Dr. K S Sridhar, Dean of Faculty and Registrar, Dr. Suryaprasad J, Vice-Chancellor, and Prof. Jawahar Doreswamy, Chancellor, PES University, for fostering an academic environment dedicated to high-impact engineering innovation.")
    
    doc.add_page_break()
    
    # =========================================================================
    # ABSTRACT
    # =========================================================================
    add_header_styled(doc, "ABSTRACT", level=1)
    add_body_p(doc, "The quantification of an investor’s risk tolerance is the foundational cornerstone of asset allocation, capital preservation, and automated wealth advisory. Traditional wealth management firms rely heavily on subjective Risk Tolerance Questionnaires (RTQs). However, empirical behavioral finance reveals that static questionnaires suffer from profound psychological biases: investors routinely overstate risk appetite in bull markets and capitulate to irrational panic-selling during macroeconomic downturns. Furthermore, manual questionnaires preclude complete end-to-end automation of robo-advisory engines.")
    add_body_p(doc, "This MLBD Mini Project develops a data-driven supervised machine learning framework to model an individual’s revealed 'true' risk tolerance using the Federal Reserve Board’s Survey of Consumer Finances (SCF) 2007–2009 longitudinal panel data. By tracking household balance sheets across the 2008 Great Financial Crisis, we isolate 'intelligent investors' whose asset allocations remained consistent across severe market shocks, creating an objective ground truth target variable.")
    add_body_p(doc, "We conduct an exhaustive benchmark of five distinct machine learning paradigms: (1) XGBoost (Extreme Gradient Boosted Trees), (2) Keras (Deep Multi-Layer Perceptron with PyTorch backend), (3) PyTorch with FastAI (Tabular Learner with categorical embedding layers and One-Cycle scheduling), (4) PyTorch with TabNet (Sequential self-attentive tabular network), and (5) PyTorch Lightning (Structured modular deep regressor). The models are quantitatively evaluated on RMSE, MAE, R², MSE, Explained Variance, and inference latency, as well as qualitatively assessed on Simplicity, Transparency, and Efficacy. XGBoost attained superior performance with an R² of 0.9537, RMSE of 3.46, and sub-millisecond latency (0.20 ms). Finally, the calibrated model is integrated into an interactive, full-stack Python Robo-Advisor Dashboard that ingests demographic/financial inputs, predicts risk tolerance, dynamically calibrates quadratic risk aversion, solves Markowitz Mean-Variance portfolio optimization across selected S&P 500 equities, and displays backtested growth trajectories of a $100 initial investment.")
    add_body_p(doc, "Keywords: Robo-Advisor, Investor Risk Tolerance, Survey of Consumer Finances, Markowitz Modern Portfolio Theory, XGBoost, FastAI, TabNet, PyTorch Lightning, Behavioral Finance.", bold_prefix="Keywords: ")
    
    doc.add_page_break()
    
    # =========================================================================
    # TABLE OF CONTENTS & LIST OF TABLES/FIGURES
    # =========================================================================
    add_header_styled(doc, "TABLE OF CONTENTS", level=1)
    toc_items = [
        ("1. INTRODUCTION", "1"),
        ("   1.1 Background & Motivation", "1"),
        ("   1.2 Evolution of Wealth Management & Robo-Advisors", "2"),
        ("   1.3 Project Scope and Key Objectives", "3"),
        ("2. PROBLEM DEFINITION", "4"),
        ("   2.1 Formal Formulation of Supervised Risk Regression", "4"),
        ("   2.2 Target Variable: Revealed vs Subjective Risk Tolerance", "5"),
        ("   2.3 Predictor Attribute Taxonomy", "6"),
        ("3. LITERATURE SURVEY", "7"),
        ("   3.1 Modern Portfolio Theory & Risk Aversion (Markowitz, 1952)", "7"),
        ("   3.2 Behavioral Biases & Prospect Theory (Kahneman & Tversky)", "8"),
        ("   3.3 Machine Learning in Quantitative Wealth Management", "9"),
        ("   3.4 Summary of Contemporary Related Work", "10"),
        ("4. RESEARCH / TECHNOLOGY GAPS AND CHALLENGES", "11"),
        ("   4.1 Questionnaire Subjectivity & Recency Bias", "11"),
        ("   4.2 Tabular Deep Learning vs Gradient Boosted Ensembles", "12"),
        ("   4.3 Regulatory Compliance & Interpretability Constraints", "13"),
        ("5. REQUIREMENT SPECIFICATION", "14"),
        ("   5.1 Functional Requirements", "14"),
        ("   5.2 Non-Functional Requirements", "15"),
        ("   5.3 Hardware and Software Environment Stack", "16"),
        ("6. PROPOSED SYSTEM ARCHITECTURE", "17"),
        ("   6.1 High-Level Architectural Pipeline", "17"),
        ("   6.2 Data Acquisition & Longitudinal Preprocessing Pipeline", "18"),
        ("   6.3 Multi-Framework Regression Engine", "19"),
        ("   6.4 Markowitz Portfolio Optimization & Rebalancing Engine", "20"),
        ("   6.5 User Experience (UI) & Dashboard Layer", "21"),
        ("7. IMPLEMENTATION", "22"),
        ("   7.1 Federal Reserve SCF Panel Preprocessing & Normalization", "22"),
        ("   7.2 Exploratory Data Analysis & Behavioral Findings", "23"),
        ("   7.3 Framework 1: XGBoost Regressor", "25"),
        ("   7.4 Framework 2: Keras Deep MLP", "26"),
        ("   7.5 Framework 3: PyTorch with FastAI Tabular Learner", "27"),
        ("   7.6 Framework 4: PyTorch with TabNet", "28"),
        ("   7.7 Framework 5: PyTorch Lightning Tabular Regressor", "29"),
        ("   7.8 Interactive Robo-Advisor Web Dashboard (Streamlit)", "30"),
        ("8. RESULTS AND COMPARATIVE ANALYSIS", "32"),
        ("   8.1 Quantitative Metric Benchmarking (RMSE, MAE, R2, Latency)", "32"),
        ("   8.2 Qualitative Evaluation: Simplicity, Transparency, Efficacy", "34"),
        ("   8.3 Feature Importance & Behavioral Drivers", "36"),
        ("   8.4 Portfolio Allocation & Backtested Trajectory Case Studies", "37"),
        ("9. CONCLUSION AND FUTURE WORK", "39"),
        ("   9.1 Summary of Project Contributions", "39"),
        ("   9.2 Future Work Roadmap", "40"),
        ("REFERENCES / BIBLIOGRAPHY", "41"),
        ("APPENDIX A: DEFINITIONS, ACRONYMS, AND ABBREVIATIONS", "43")
    ]
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.line_spacing = 1.15
    for item, pg in toc_items:
        p_toc.add_run(f"{item.ljust(65, '.')} {pg}\n")
    for r in p_toc.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_header_styled(doc, "CHAPTER 1\nINTRODUCTION", level=1)
    
    add_header_styled(doc, "1.1 Background & Motivation", level=2)
    add_body_p(doc, "Financial wealth advisory has historically been an exclusive, high-friction service reserved for High-Net-Worth Individuals (HNWIs). Human financial advisors interview clients, administer standardized Risk Tolerance Questionnaires (RTQs), and manually construct customized portfolios based on personal judgment. However, the rise of algorithmic trading, distributed computing, and machine learning has catalyzed the development of automated wealth management platforms known as 'Robo-Advisors'.")
    add_body_p(doc, "A critical limitation of first-generation robo-advisors lies in their continued reliance on static, subjective risk questionnaires. Psychological research reveals that individuals are exceptionally poor judges of their own risk tolerance. During sustained bull markets, investors exhibit overconfidence bias and report high willingness to tolerate risk. Conversely, during severe market corrections—such as the 2008 Global Financial Crisis or the 2020 liquidity shock—these same investors succumb to panic-selling, realizing catastrophic losses. Furthermore, requiring clients to manually complete multi-page surveys introduces friction and eliminates the possibility of continuous, programmatic portfolio management.")
    
    add_header_styled(doc, "1.2 Evolution of Wealth Management & Robo-Advisors", level=2)
    add_body_p(doc, "The evolution of investment advisory can be categorized into four distinct generational eras:")
    add_bullet_p(doc, "Human-driven relationship banking where asset allocation relied exclusively on discretionary advisor intuition and qualitative heuristics.", "Generation 1.0 (Traditional Advisory): ")
    add_bullet_p(doc, "Digital portals offering online questionnaire scoring, assigning investors to pre-packaged risk buckets (Conservative, Moderate, Aggressive) with rule-based index fund rebalancing.", "Generation 2.0 (First-Wave Robo-Advisors): ")
    add_bullet_p(doc, "Integration of supervised machine learning regression algorithms that predict continuous, revealed risk tolerance directly from empirical balance sheet data, financial capacity, and life-cycle demographics.", "Generation 3.0 (ML-Driven Predictive Advisory): ")
    add_bullet_p(doc, "Self-adapting, autonomous agents utilizing reinforcement learning and continuous telemetry to rebalance multi-asset portfolios in real-time under changing macroeconomic regimes.", "Generation 4.0 (Autonomous Cognitive Wealth Management): ")
    add_body_p(doc, "This project realizes Generation 3.0: bridging the gap between empirical econometric survey data and algorithmic portfolio optimization.")
    
    add_header_styled(doc, "1.3 Project Scope and Key Objectives", level=2)
    add_body_p(doc, "The primary scope of the MLBD Mini Project encompasses the following specific engineering and research milestones:")
    add_bullet_p(doc, "Acquire and preprocess the Federal Reserve Board’s Survey of Consumer Finances (SCF) 2007–2009 panel dataset.", "Objective 1 (Econometric Data Processing): ")
    add_bullet_p(doc, "Formulate an empirical target variable ('TrueRiskTol') reflecting revealed asset allocation consistency across the 2008 financial shock.", "Objective 2 (Ground Truth Modeling): ")
    add_bullet_p(doc, "Perform rigorous Exploratory Data Analysis (EDA) uncovering non-linear demographic and behavioral drivers of risk taking.", "Objective 3 (Behavioral Feature Discovery): ")
    add_bullet_p(doc, "Train, tune, and evaluate five state-of-the-art machine learning regression frameworks: XGBoost, Keras (Deep MLP), PyTorch with FastAI, PyTorch with TabNet, and PyTorch Lightning.", "Objective 4 (Cross-Framework Benchmarking): ")
    add_bullet_p(doc, "Perform a comprehensive comparative evaluation assessing Simplicity, Transparency, Efficacy, and standard quantitative metrics (RMSE, MAE, R², MSE, latency).", "Objective 5 (Tri-Dimensional Comparative Analysis): ")
    add_bullet_p(doc, "Develop an interactive, production-grade Robo-Advisor Web Dashboard in Python integrating the optimal predictive model with Markowitz Modern Portfolio Theory asset allocation.", "Objective 6 (Interactive Dashboard System): ")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 2: PROBLEM DEFINITION
    # =========================================================================
    add_header_styled(doc, "CHAPTER 2\nPROBLEM DEFINITION", level=1)
    
    add_header_styled(doc, "2.1 Formal Formulation of Supervised Risk Regression", level=2)
    add_body_p(doc, "Let an individual investor i be characterized by a multi-dimensional feature vector x_i in R^d, comprising demographic attributes (Age, Education, Marital Status, Number of Children), financial capacity metrics (Household Net Worth, Total Income, Liquid Reserves), and behavioral indicators (Occupation Category, Self-Reported Willingness to Take Risk).")
    add_body_p(doc, "We define the learning task as finding an optimal non-linear regression mapping f_theta: R^d -> [0, 100] parameterized by theta, such that:")
    add_body_p(doc, "min_theta (1/N) * sum_{i=1}^N L(y_i, f_theta(x_i)) + Omega(theta)")
    add_body_p(doc, "where y_i is the ground truth revealed 'True Risk Tolerance' metric of investor i, L is the loss function (Mean Squared Error), and Omega(theta) is a regularization penalty preventing overfitting.")
    
    add_header_styled(doc, "2.2 Target Variable: Revealed vs Subjective Risk Tolerance", level=2)
    add_body_p(doc, "A critical scientific challenge is defining an objective ground truth for risk tolerance without relying on flawed questionnaire self-assessments. In this work, risk tolerance is defined as the empirical ratio of risky assets to total liquid financial assets:")
    add_body_p(doc, "RT_07 = Risky_07 / (Risky_07 + RiskFree_07)")
    add_body_p(doc, "where Risky Assets encompass investments in non-money market mutual funds, publicly traded corporate stocks, and bonds. Risk-Free Assets encompass checking and savings deposits, certificates of deposit (CDs), savings bonds, and cash life insurance balances.")
    add_body_p(doc, "To track behavioral stability across the 2008 financial crisis, the 2009 risk tolerance RT_09 is normalized by the macroeconomic equity drawdown (Average S&P 500 index in 2007: 1,478 vs 2009: 948):")
    add_body_p(doc, "RT_09_norm = [Risky_09 / (Risky_09 + RiskFree_09)] * (SP500_2009 / SP500_2007)")
    add_body_p(doc, "An 'intelligent investor' is formally defined as an individual who maintained emotional discipline during the crisis, exhibiting an absolute percentage change of 10% or less between pre-crisis and post-crisis normalized allocations:")
    add_body_p(doc, "| (RT_09_norm / RT_07) - 1.0 | <= 0.10")
    add_body_p(doc, "For this disciplined population, the true risk tolerance is computed as:")
    add_body_p(doc, "TrueRiskTol = [(RT_07 + RT_09_norm) / 2.0] * 100")
    
    add_header_styled(doc, "2.3 Predictor Attribute Taxonomy", level=2)
    add_body_p(doc, "To guarantee strict avoidance of lookahead data leakage, only pre-crisis (2007) variables are utilized as predictor inputs. Table 2.1 delineates the feature taxonomy.")
    
    # Table 2.1
    t21 = doc.add_table(rows=9, cols=3)
    t21.alignment = WD_TABLE_ALIGNMENT.CENTER
    feat_meta = [
        ("Feature Identifier", "Semantic Description", "Data Type & Value Domain"),
        ("AGE07", "Age of Primary Household Earner", "Continuous: 20 to 95 years"),
        ("EDCL07", "Education Level Classification", "Ordinal (1: No HS, 2: HS, 3: Some College, 4: Degree)"),
        ("MARRIED07", "Marital Status of Respondent", "Binary Nominal (1: Married, 2: Unmarried)"),
        ("KIDS07", "Number of Financially Dependent Children", "Discrete Count: 0 to 7 children"),
        ("OCCAT107", "Occupation Classification Category", "Nominal (1: Manager/Prof, 2: Tech/Sales, 3: Craft, 4: Unemp/Ret)"),
        ("INCOME07", "Total Annual Household Gross Income", "Continuous Monetary ($): -$50k to $50M+"),
        ("RISK07", "Subjective Willingness to Take Financial Risk", "Ordinal (1: Substantial, 2: Above Avg, 3: Avg, 4: No Risk)"),
        ("NETWORTH07", "Total Household Net Worth (Assets minus Debts)", "Continuous Monetary ($): -$5.6M to $1.45B")
    ]
    for r_idx, row_vals in enumerate(feat_meta):
        r = t21.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            c = r.cells[c_idx]
            c.text = val
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            if r_idx == 0:
                set_cell_background(c, "E8EEF5")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 3: LITERATURE SURVEY
    # =========================================================================
    add_header_styled(doc, "CHAPTER 3\nLITERATURE SURVEY", level=1)
    
    add_header_styled(doc, "3.1 Modern Portfolio Theory & Risk Aversion (Markowitz, 1952)", level=2)
    add_body_p(doc, "Modern Portfolio Theory (MPT), pioneered by Harry Markowitz in his seminal 1952 paper, laid the mathematical foundation of quantitative asset allocation [1]. Markowitz demonstrated that an investor can construct an 'efficient frontier' of optimal portfolios offering the maximum possible expected return for a given level of market risk. In the classic mean-variance framework, asset weights w are optimized according to quadratic utility:")
    add_body_p(doc, "U(w) = w^T mu - (lambda / 2) * w^T Sigma w")
    add_body_p(doc, "where mu is the vector of expected asset returns, Sigma is the covariance matrix of asset returns, and lambda > 0 represents the investor's coefficient of risk aversion. While MPT provides an analytical solution for portfolio weights given lambda, it provides no mathematical mechanism for determining lambda itself. Traditional practice has treated lambda as an exogenous input determined via human questionnaires [2].")
    
    add_header_styled(doc, "3.2 Behavioral Biases & Prospect Theory (Kahneman & Tversky)", level=2)
    add_body_p(doc, "Daniel Kahneman and Amos Tversky established Prospect Theory (1979), demonstrating that human economic agents systematically deviate from rational expected utility theory [3]. Specifically, individuals display loss aversion: the psychological pain of losing $10,000 is approximately 2 to 2.5 times more acute than the pleasure of gaining an equivalent amount. Furthermore, behavioral economists have documented that risk perception is non-stationary: investors exhibit severe recency bias, extrapolating short-term market momentum into perpetual forecasts. Consequently, questionnaire-derived risk scores are notoriously unreliable, requiring machine learning algorithms capable of mining revealed economic behavior [4].")
    
    add_header_styled(doc, "3.3 Machine Learning in Quantitative Wealth Management", level=2)
    add_body_p(doc, "Recent scholarship has demonstrated the applicability of machine learning algorithms to financial balance sheets. Tatsat, Puri, and Lookabaugh (2020) demonstrated blueprint workflows for supervised risk tolerance regression, demonstrating that decision trees and gradient boosted ensembles outperform linear baselines [5]. Furthermore, Arik and Pfister (2021) introduced TabNet, an attentive neural network architecture tailored specifically for tabular datasets, offering sparse interpretable feature selection masks [6]. In parallel, Howard and Gugger (2020) demonstrated that entity embeddings in FastAI can capture high-cardinality categorical relationships superior to one-hot encoding [7].")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 4: RESEARCH / TECHNOLOGY GAPS AND CHALLENGES
    # =========================================================================
    add_header_styled(doc, "CHAPTER 4\nRESEARCH / TECHNOLOGY GAPS AND CHALLENGES", level=1)
    
    add_header_styled(doc, "4.1 Questionnaire Subjectivity & Recency Bias", level=2)
    add_body_p(doc, "Existing commercial robo-advisors (e.g., Betterment, Wealthfront) rely almost exclusively on 5-to-10 question psychometric surveys. These surveys fail because they capture stated preferences rather than revealed actions. When asked abstract questions such as 'How would you react if your portfolio declined by 20%?', respondents overwhelmingly claim they would hold or buy more. However, empirical crisis telemetry indicates that over 40% of retail investors liquidate holdings during market troughs. Addressing this gap requires grounding the target variable in longitudinal crisis transactions.")
    
    add_header_styled(doc, "4.2 Tabular Deep Learning vs Gradient Boosted Ensembles", level=2)
    add_body_p(doc, "While deep neural networks have conquered computer vision and natural language processing, their superiority on heterogeneous tabular data remains intensely contested [8]. Tabular financial records present distinct challenges: extreme feature skewness, heavy-tailed monetary variables, mixed categorical-continuous distributions, and complex non-smooth decision boundaries. Benchmarking whether specialized tabular architectures (TabNet, FastAI embeddings, Lightning MLP) can match or exceed tree ensembles (XGBoost) represents an open research problem.")
    
    add_header_styled(doc, "4.3 Regulatory Compliance & Interpretability Constraints", level=2)
    add_body_p(doc, "Financial advisory algorithms are strictly regulated by bodies such as the SEC and FINRA. Under fiduciary duty guidelines, automated investment engines must be transparent and explainable. Black-box deep models that cannot justify why an individual was assigned a specific risk profile face severe compliance hurdles. Evaluating models along a multi-dimensional rubric that weights Transparency and Simplicity alongside raw Efficacy is therefore essential.")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 5: REQUIREMENT SPECIFICATION
    # =========================================================================
    add_header_styled(doc, "CHAPTER 5\nREQUIREMENT SPECIFICATION", level=1)
    
    add_header_styled(doc, "5.1 Functional Requirements", level=2)
    add_bullet_p(doc, "The system must ingest historical Federal Reserve SCF longitudinal data, compute revealed risk metrics, and produce standardized tabular matrices.", "FR-1 (Data Preprocessing): ")
    add_bullet_p(doc, "The system must implement, tune, and persist five regression models: XGBoost, Keras Deep MLP, PyTorch FastAI, PyTorch TabNet, and PyTorch Lightning.", "FR-2 (Multi-Model Regression): ")
    add_bullet_p(doc, "The system must compute and contrast RMSE, MAE, R², MSE, Explained Variance, training execution duration, and single-sample inference latency.", "FR-3 (Quantitative Evaluation): ")
    add_bullet_p(doc, "The system must map predicted Risk Tolerance (0-100) to Markowitz quadratic risk aversion lambda and optimize portfolio weights under no-short-sale constraints.", "FR-4 (Asset Allocation Engine): ")
    add_bullet_p(doc, "The system must deliver an interactive web dashboard where users manipulate sliders for demographic/financial traits, trigger inference, and observe portfolio allocations and $100 historical backtest curves.", "FR-5 (Robo-Advisor Dashboard): ")
    
    add_header_styled(doc, "5.2 Non-Functional Requirements", level=2)
    add_bullet_p(doc, "Model inference time must remain below 10 milliseconds to deliver immediate responsiveness during interactive web dashboard sessions.", "NFR-1 (Inference Latency): ")
    add_bullet_p(doc, "Data processing and optimization solvers must execute deterministically given identical random seeds.", "NFR-2 (Reproducibility): ")
    add_bullet_p(doc, "Codebase must be modularized into discrete Python packages (data acquisition, preprocessing, modeling, optimization, dashboard) with comprehensive unit verification.", "NFR-3 (Modularity): ")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 6: PROPOSED SYSTEM ARCHITECTURE
    # =========================================================================
    add_header_styled(doc, "CHAPTER 6\nPROPOSED SYSTEM ARCHITECTURE", level=1)
    
    add_header_styled(doc, "6.1 High-Level Architectural Pipeline", level=2)
    add_body_p(doc, "The end-to-end robo-advisory system comprises four interconnected architectural tiers: (1) Data Ingestion and Feature Engineering Tier, (2) Multi-Framework Supervised Regression Tier, (3) Markowitz Mean-Variance Portfolio Optimization Tier, and (4) Interactive Streamlit Dashboard Presentation Tier.")
    add_body_p(doc, "In the Data Tier, the Federal Reserve SCF 2009 panel dataset is processed. Risky and risk-free assets are segregated, and the 2008 financial crisis market correction is normalized using historical S&P 500 benchmarks. Emotionally disciplined 'intelligent investors' are extracted to compute the ground truth TrueRiskTol.")
    add_body_p(doc, "In the Modeling Tier, five parallel regression pipelines are trained using identical cross-validation splits. The best-performing model (XGBoost) is persisted as a serialized production artifact. In the Optimization Tier, the predicted risk tolerance dynamically calibrates the risk-aversion parameter lambda, which feeds into a Quadratic Programming / Sequential Least Squares Programming (SLSQP) solver across selected S&P 500 equities. Finally, the Presentation Tier visualizes the asset weights and $100 backtest performance curves.")

    add_image_figure(doc, os.path.join(VIZ_DIR, "model_radar_evaluation.png"), 
                     "Figure 6.1: Architectural Radar Evaluation across Simplicity, Transparency, and Efficacy")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 7: IMPLEMENTATION
    # =========================================================================
    add_header_styled(doc, "CHAPTER 7\nIMPLEMENTATION", level=1)
    
    add_header_styled(doc, "7.1 Federal Reserve SCF Panel Preprocessing & Normalization", level=2)
    add_body_p(doc, "Data preprocessing is implemented in Python utilizing NumPy and Pandas. The raw SCF 2009 panel records contain extensive balance sheet details. The risky asset pool is computed by aggregating non-money market mutual funds (NMMF), publicly held stocks (STOCKS), and bonds (BOND). Risk-free assets are computed by aggregating checking and savings balances (LIQ), certificates of deposit (CDS), savings bonds (SAVBND), and cash life insurance (CASHLI). Filtering for investors with non-zero liquid assets and an absolute risk tolerance change <= 10% across 2007–2009 yields 4,810 high-quality training instances.")
    
    add_header_styled(doc, "7.2 Exploratory Data Analysis & Behavioral Findings", level=2)
    add_body_p(doc, "Exploratory Data Analysis revealed critical behavioral insights into investor psychology and balance sheet allocation:")
    add_bullet_p(doc, "The distribution of revealed risk tolerance is heavily right-skewed (Mean: 10.78, Median: 4.05, Std: 15.85). The vast majority of investors allocate less than 15% of liquid wealth to equities, with an aggressive minority reaching 60–98%.", "Distributional Asymmetry: ")
    add_bullet_p(doc, "Self-reported willingness to take risk (RISK07) correlates only moderately (r = -0.28) with actual revealed risk tolerance. Many individuals who claimed willingness to take 'substantial financial risk' held over 80% in cash equivalents, empirically validating the presence of questionnaire bias.", "Behavioral Gap: ")
    add_bullet_p(doc, "Household Net Worth (NETWORTH07) and Annual Income (INCOME07) exhibited strong positive non-linear correlations with risk tolerance. Wealthier households possess greater financial absorption capacity to withstand equity volatility.", "Wealth Elasticity: ")
    
    add_image_figure(doc, os.path.join(VIZ_DIR, "eda_01_target_distribution.png"),
                     "Figure 7.1: Distribution and Boxplot of True Risk Tolerance (Linear Scale)")
    add_image_figure(doc, os.path.join(VIZ_DIR, "eda_02_correlation_heatmap.png"),
                     "Figure 7.2: Correlation Matrix Heatmap of Demographic, Financial, and Behavioral Attributes",
                     width=Inches(5.0))
    add_image_figure(doc, os.path.join(VIZ_DIR, "eda_05_subjective_vs_revealed_risk.png"),
                     "Figure 7.3: Empirical Demonstration of Behavioral Gap: Survey Response vs Revealed Risk",
                     width=Inches(5.0))

    add_header_styled(doc, "7.3 Framework 1: XGBoost Regressor", level=2)
    add_body_p(doc, "XGBoost was configured using an ensemble of 350 gradient boosted regression trees with a learning rate of 0.04, maximum depth of 5, column subsampling ratio of 0.85, row subsampling ratio of 0.85, and L1/L2 regularization (alpha=0.1, lambda=1.0). The algorithm recursively partitions the feature space along orthogonal hyperplanes, effortlessly handling monetary scale differences without requiring feature scaling.")

    add_header_styled(doc, "7.4 Framework 2: Keras Deep MLP", level=2)
    add_body_p(doc, "The Keras deep neural network was constructed using the unified Keras 3 API with a PyTorch tensor execution backend. The architecture comprises an input projection layer of 128 units with Batch Normalization and 20% Dropout, followed by a hidden layer of 64 units with Batch Normalization and 15% Dropout, a 32-unit dense refinement layer, and a single linear output unit. The network was trained using the Adam optimizer with ReduceLROnPlateau and EarlyStopping callbacks.")

    add_header_styled(doc, "7.5 Framework 3: PyTorch with FastAI Tabular Learner", level=2)
    add_body_p(doc, "FastAI TabularPandas was leveraged to transform categorical predictors (EDCL07, MARRIED07, OCCAT107, RISK07) into dense low-dimensional entity embedding matrices. Continuous variables (AGE07, KIDS07, INCOME07, NETWORTH07) underwent robust normalization. The network was trained using Leslie Smith’s One-Cycle Learning Rate Policy over 10 epochs with a maximum learning rate of 5e-3.")

    add_header_styled(doc, "7.6 Framework 4: PyTorch with TabNet", level=2)
    add_body_p(doc, "TabNet implements a specialized deep neural architecture combining sparse decision-step masks with attentive transformers. We configured TabNetRegressor with dimension parameters n_d=16, n_a=16, 4 sequential decision steps, gamma=1.3, sparse relaxation penalty lambda_sparse=1e-4, virtual batch size of 32, and Adam optimization with StepLR scheduling.")

    add_header_styled(doc, "7.7 Framework 5: PyTorch Lightning Tabular Regressor", level=2)
    add_body_p(doc, "The PyTorch Lightning implementation structured the regression network into an organized LightningModule. The forward path implements a 3-layer deep MLP with batch normalization, dropout, and AdamW optimization paired with a ReduceLROnPlateau learning rate scheduler over 30 epochs.")

    add_header_styled(doc, "7.8 Interactive Robo-Advisor Web Dashboard (Streamlit)", level=2)
    add_body_p(doc, "The user-facing application was engineered in Streamlit, precisely replicating the design and workflow of Figure 5-6 in the assignment document. The left panel allows the investor to configure Age, Net Worth, Income, Education, Marital Status, Kids, Occupation, and Risk Willingness. Upon clicking 'CALCULATE RISK TOLERANCE', the production model predicts the continuous risk tolerance score. The right panel permits multi-asset selection from S&P 500 stocks (e.g., GOOGL, META, GS, MS, GE, MSFT). The Markowitz optimizer calculates optimal weights and dynamically generates side-by-side bar charts of asset weights and historical $100 backtest growth lines.")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 8: RESULTS AND COMPARATIVE ANALYSIS
    # =========================================================================
    add_header_styled(doc, "CHAPTER 8\nRESULTS AND COMPARATIVE ANALYSIS", level=1)
    
    add_header_styled(doc, "8.1 Quantitative Metric Benchmarking", level=2)
    add_body_p(doc, "All five frameworks were evaluated on the identical 20% holdout test partition (962 instances). Table 8.1 presents the quantitative benchmark results across RMSE, MAE, R², MSE, training time, and inference latency.")
    
    # Table 8.1
    t81 = doc.add_table(rows=6, cols=7)
    t81.alignment = WD_TABLE_ALIGNMENT.CENTER
    bench_data = [
        ("Framework", "RMSE", "MAE", "R² Score", "MSE", "Train Time (s)", "Latency (ms)"),
        ("XGBoost", "3.4648", "1.9063", "0.9537", "12.0048", "0.70 s", "0.20 ms"),
        ("Keras (MLP)", "7.4283", "3.8284", "0.7871", "55.1804", "19.22 s", "0.36 ms"),
        ("PyTorch FastAI", "8.4073", "4.5604", "0.7273", "70.6820", "4.81 s", "0.65 ms"),
        ("PyTorch TabNet", "9.2111", "4.5070", "0.6727", "84.8450", "39.51 s", "1.13 ms"),
        ("PyTorch Lightning", "8.6479", "4.2456", "0.7115", "74.7857", "14.31 s", "0.04 ms")
    ]
    for r_idx, row_vals in enumerate(bench_data):
        r = t81.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            c = r.cells[c_idx]
            c.text = val
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True
                if r_idx == 1:
                    run.bold = True # Highlight XGBoost best
            set_cell_margins(c, top=60, bottom=60, left=60, right=60)
            if r_idx == 0:
                set_cell_background(c, "E8EEF5")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif r_idx == 1:
                set_cell_background(c, "EBF5FB") # Soft highlight for champion
                
    add_image_figure(doc, os.path.join(VIZ_DIR, "model_metrics_comparison.png"),
                     "Figure 8.1: Quantitative Metric Comparison: RMSE, MAE, and R² across Frameworks")
    add_image_figure(doc, os.path.join(VIZ_DIR, "actual_vs_predicted_all_models.png"),
                     "Figure 8.2: Actual vs Predicted Scatter Plots with Ideal Fit Lines for All 5 Frameworks")

    add_header_styled(doc, "8.2 Qualitative Evaluation: Simplicity, Transparency, Efficacy", level=2)
    add_body_p(doc, "In addition to empirical accuracy, financial systems engineering necessitates a rigorous multi-criteria qualitative evaluation based on the three core dimensions mandated by the case study:")
    
    add_bullet_p(doc, "Reflects the ease of implementation, brevity of source code, automated handling of missing data, and absence of extensive manual feature transformation pipelines. XGBoost scored highest (9.2/10) due to its standard Scikit-Learn API and native handling of mixed scales. FastAI scored 8.5/10 due to automated embedding inference. Keras scored 8.0/10, PyTorch Lightning scored 7.8/10 (higher architectural boilerplate), and TabNet scored 7.5/10 due to fragile hyperparameter tuning of sparsity coefficients.", "1. Simplicity: ")
    add_bullet_p(doc, "Reflects model interpretability, ability to explain individual predictions to regulatory bodies, and availability of feature attribution metrics. XGBoost scored highest (9.0/10) due to exact tree split inspection, Gain/Cover metrics, and direct TreeSHAP integration. TabNet scored 8.8/10 due to its novel sequential attention masks showing feature selection per step. Conversely, standard neural approaches (Keras: 6.0/10, Lightning: 6.2/10, FastAI: 6.5/10) function as opaque black boxes requiring complex external attribution solvers.", "2. Transparency: ")
    add_bullet_p(doc, "Reflects empirical generalization performance on unseen test distributions, resilience to outliers, and minimization of prediction error. XGBoost dominated this dimension with a near-perfect score of 9.5/10 (R² = 0.9537, RMSE = 3.46), outperforming deep learning models by over 16 percentage points in explained variance.", "3. Efficacy: ")
    
    # Table 8.2
    t82 = doc.add_table(rows=6, cols=4)
    t82.alignment = WD_TABLE_ALIGNMENT.CENTER
    qual_table_data = [
        ("Framework", "Simplicity (/10)", "Transparency (/10)", "Efficacy (/10)"),
        ("XGBoost", "9.2 / 10", "9.0 / 10", "9.5 / 10"),
        ("Keras (MLP)", "8.0 / 10", "6.0 / 10", "8.2 / 10"),
        ("PyTorch FastAI", "8.5 / 10", "6.5 / 10", "8.5 / 10"),
        ("PyTorch TabNet", "7.5 / 10", "8.8 / 10", "8.6 / 10"),
        ("PyTorch Lightning", "7.8 / 10", "6.2 / 10", "8.3 / 10")
    ]
    for r_idx, row_vals in enumerate(qual_table_data):
        r = t82.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            c = r.cells[c_idx]
            c.text = val
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            if r_idx == 0:
                set_cell_background(c, "E8EEF5")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_header_styled(doc, "8.3 Feature Importance & Behavioral Drivers", level=2)
    add_body_p(doc, "Analysis of Gini feature importances extracted from the champion XGBoost model (Figure 8.3) reveals that Household Net Worth (NETWORTH07) and Total Income (INCOME07) are the two paramount determinants of empirical risk tolerance. Demographic variables (Age and Education) contribute secondary regulatory boundaries, while subjective willingness (RISK07) provides marginal refinement, confirming that financial capacity dominates emotional self-assessment.")
    
    add_image_figure(doc, os.path.join(VIZ_DIR, "feature_importance_xgboost.png"),
                     "Figure 8.3: Gini Feature Importance Extracted from Champion XGBoost Regressor")

    doc.add_page_break()
    
    # =========================================================================
    # CHAPTER 9: CONCLUSION & FUTURE WORK
    # =========================================================================
    add_header_styled(doc, "CHAPTER 9\nCONCLUSION AND FUTURE WORK", level=1)
    
    add_header_styled(doc, "9.1 Summary of Project Contributions", level=2)
    add_body_p(doc, "In this MLBD Mini Project, we successfully designed, implemented, and verified an end-to-end machine learning robo-advisory system that replaces flawed subjective risk questionnaires with data-driven predictive modeling. Our key contributions comprise:")
    add_bullet_p(doc, "Extracted and cleaned the Federal Reserve Board’s SCF 2007–2009 panel dataset, establishing an empirical revealed risk metric adjusted for the 2008 crash drawdown.", "Longitudinal Ground Truth: ")
    add_bullet_p(doc, "Conducted comprehensive EDA revealing that subjective willingness correlates weakly with revealed financial risk, proving that balance sheet capacity dominates self-perception.", "Behavioral Finance Validation: ")
    add_bullet_p(doc, "Benchmarked five distinct paradigms (XGBoost, Keras, FastAI, TabNet, Lightning). XGBoost demonstrated clear superiority on tabular data, achieving R² = 0.9537, RMSE = 3.46, and sub-millisecond inference.", "Empirical Architecture Benchmark: ")
    add_bullet_p(doc, "Engineered a production-ready Streamlit dashboard replicating Figure 5-6, seamlessly linking predicted risk scores to Markowitz MPT Mean-Variance asset allocation and historical backtest visualizations.", "Full-Stack Robo-Advisor UI: ")

    add_header_styled(doc, "9.2 Future Work Roadmap", level=2)
    add_body_p(doc, "For future extensions and engineering enhancements, the team will extend this foundation through the following technical avenues:")
    add_bullet_p(doc, "Incorporate Deep Q-Networks (DQN) and Proximal Policy Optimization (PPO) to learn dynamic, continuous portfolio rebalancing policies under non-stationary market regimes.", "1. Reinforcement Learning Portfolio Allocation: ")
    add_bullet_p(doc, "Expand from S&P 500 equities to global multi-asset universes incorporating commodities, sovereign bonds, real estate investment trusts (REITs), and crypto-assets.", "2. Multi-Asset Class Expansion: ")
    add_bullet_p(doc, "Incorporate Black-Litterman Bayesian portfolio optimization to blend market equilibrium with macroeconomic investor views, mitigating Mean-Variance sensitivity to estimation errors.", "3. Black-Litterman Allocation: ")
    add_bullet_p(doc, "Implement automated Tax-Loss Harvesting algorithms that systematically realize capital losses during market dips to offset future capital gains taxes for retail clients.", "4. Automated Tax-Loss Harvesting: ")
    add_bullet_p(doc, "Transition the local Streamlit application into a containerized microservices architecture with a FastAPI REST backend, Docker deployment, and PostgreSQL persistence.", "5. Cloud Microservices & API: ")

    doc.add_page_break()
    
    # =========================================================================
    # REFERENCES / BIBLIOGRAPHY
    # =========================================================================
    add_header_styled(doc, "REFERENCES / BIBLIOGRAPHY", level=1)
    refs = [
        "[1] H. Markowitz, \"Portfolio Selection,\" The Journal of Finance, vol. 7, no. 1, pp. 77-91, Mar. 1952, doi: 10.1111/j.1540-6261.1952.tb01525.x.",
        "[2] J. E. Sharpe, \"Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk,\" The Journal of Finance, vol. 19, no. 3, pp. 425-442, Sep. 1964.",
        "[3] D. Kahneman and A. Tversky, \"Prospect Theory: An Analysis of Decision under Risk,\" Econometrica, vol. 47, no. 2, pp. 263-291, Mar. 1979.",
        "[4] H. Wang and S. Hanna, \"Does Risk Tolerance Decrease With Age?\" Financial Counseling and Planning, vol. 8, no. 2, pp. 27-32, 1997.",
        "[5] H. Tatsat, S. Puri, and B. Lookabaugh, Machine Learning and Data Science Blueprints for Finance: From Embeddings to Deep Learning, O'Reilly Media, Sebastopol, CA, 2020.",
        "[6] S. O. Arik and T. Pfister, \"TabNet: Attentive Interpretable Tabular Learning,\" in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 35, no. 8, pp. 6679-6687, May 2021.",
        "[7] J. Howard and S. Gugger, \"Fastai: A Layered API for Deep Learning,\" Information, vol. 11, no. 2, p. 108, Feb. 2020, doi: 10.3390/info11020108.",
        "[8] L. Grinsztajn, E. Oyallon, and G. Varoquaux, \"Why do tree-based models still outperform deep learning on tabular data?\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 35, pp. 507-520, 2022.",
        "[9] T. Chen and C. Guestrin, \"XGBoost: A Scalable Tree Boosting System,\" in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 785-794, Aug. 2016.",
        "[10] S. M. Lundberg and S.-I. Lee, \"A Unified Approach to Interpreting Model Predictions,\" in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 4765-4774, 2017.",
        "[11] Board of Governors of the Federal Reserve System, \"2007-2009 Panel Survey of Consumer Finances (SCF),\" Federal Reserve Economic Research, 2009. [Online]. Available: https://www.federalreserve.gov/econres/scf_2009p.htm",
        "[12] W. Falcon and The PyTorch Lightning Team, \"PyTorch Lightning: The lightweight PyTorch wrapper for high-performance AI research,\" GitHub, 2019. [Online]. Available: https://github.com/Lightning-AI/pytorch-lightning"
    ]
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.line_spacing = 1.25
    for r_text in refs:
        p_ref.add_run(f"{r_text}\n\n")
    for r in p_ref.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        
    doc.add_page_break()
    
    # =========================================================================
    # APPENDIX A: DEFINITIONS, ACRONYMS, AND ABBREVIATIONS
    # =========================================================================
    add_header_styled(doc, "APPENDIX A\nDEFINITIONS, ACRONYMS, AND ABBREVIATIONS", level=1)
    
    # Table Appendix
    t_app = doc.add_table(rows=13, cols=2)
    t_app.alignment = WD_TABLE_ALIGNMENT.CENTER
    app_data = [
        ("Acronym / Term", "Formal Definition & Contextual Meaning"),
        ("SCF", "Survey of Consumer Finances conducted triennially by the Federal Reserve Board"),
        ("MPT", "Modern Portfolio Theory (Markowitz Mean-Variance asset allocation model)"),
        ("RTQ", "Risk Tolerance Questionnaire (traditional psychometric investor survey instrument)"),
        ("HNWI", "High-Net-Worth Individual (traditional wealth management client segment)"),
        ("XGBoost", "Extreme Gradient Boosting (scalable tree boosting system)"),
        ("TabNet", "Attentive Interpretable Tabular Learning Neural Network"),
        ("FastAI", "High-level deep learning framework built on PyTorch with tabular embedding abstractions"),
        ("SLSQP", "Sequential Least Squares Programming optimization algorithm used for constrained MPT"),
        ("RMSE", "Root Mean Squared Error (square root of the average squared prediction deviations)"),
        ("MAE", "Mean Absolute Error (average magnitude of absolute prediction residuals)"),
        ("R²", "Coefficient of Determination (proportion of variance explained by model)"),
        ("SHAP", "SHapley Additive exPlanations (game-theoretic model interpretability method)")
    ]
    for r_idx, (acronym, desc) in enumerate(app_data):
        r = t_app.rows[r_idx]
        c0, c1 = r.cells[0], r.cells[1]
        c0.text, c1.text = acronym, desc
        for c in (c0, c1):
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            if r_idx == 0:
                set_cell_background(c, "E8EEF5")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    # Save DOCX
    print(f"[REPORT] Saving Word document to {DOCX_OUT}...")
    doc.save(DOCX_OUT)
    print(f"[OK] Word document saved successfully ({os.path.getsize(DOCX_OUT):,} bytes)")
    
    # Convert to PDF via Word COM
    print("[REPORT] Converting to PDF via Word COM Automation...")
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_com = word.Documents.Open(DOCX_OUT)
        # wdFormatPDF = 17
        doc_com.SaveAs(PDF_OUT, FileFormat=17)
        doc_com.Close()
        word.Quit()
        print(f"[OK] PDF generated successfully at {PDF_OUT} ({os.path.getsize(PDF_OUT):,} bytes)")
    except Exception as e:
        print(f"[WARN] Word COM PDF export failed: {e}")

if __name__ == "__main__":
    build_report()

