#!/usr/bin/env python3
"""
Export the 350-Pair Ground Truth Benchmark Dataset into a formatted Excel Workbook.

Features:
- Sheet 1: "Master 350 Review" (complete dataset with frozen headers, formatted columns, and Is_Contradiction flag)
- Sheet 2: "Contradictions Only (116)" (isolated subset for rapid review of legal conflicts)
- Sheet 3: "Domain & Tier Summary" (pivot summary table of distribution metrics)
"""

import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSONL_PATH = os.path.join(ROOT_DIR, "data", "ground_truth_350.jsonl")
EXCEL_PATH = os.path.join(ROOT_DIR, "data", "ground_truth_350_review.xlsx")

def build_excel_review():
    print(f"Loading master dataset from: {JSONL_PATH}")
    with open(JSONL_PATH, "r", encoding="utf-8") as f:
        pairs = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(pairs)} pairs. Creating Excel workbook...")
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    fill_header = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Dark Navy
    fill_subhead = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
    
    font_contra_badge = Font(name="Calibri", size=11, bold=True, color="9C0006")
    fill_contra_badge = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid") # Soft Red
    
    font_entail_badge = Font(name="Calibri", size=11, bold=True, color="006100")
    fill_entail_badge = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid") # Soft Green
    
    font_neutral_badge = Font(name="Calibri", size=11, bold=True, color="9C6500")
    fill_neutral_badge = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid") # Soft Yellow

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    align_center = Alignment(horizontal='center', vertical='top', wrap_text=True)
    align_left = Alignment(horizontal='left', vertical='top', wrap_text=True)

    # Columns configuration
    columns = [
        ("Pair_ID", 12, align_center),
        ("Is_Contradiction?", 20, align_center),
        ("Presumed_Answer", 16, align_center),
        ("Contradiction_Mechanism / Summary", 38, align_left),
        ("Difficulty_Tier", 24, align_center),
        ("Macro_Legal_Domain", 30, align_left),
        ("Statute_Title", 28, align_left),
        ("Exact_Citation", 20, align_center),
        ("National_Statute_Premise_Text", 45, align_left),
        ("Ordinance_Hypothesis_Text", 45, align_left),
        ("Ordinance_Context_Provenance", 32, align_left),
        ("Full_Presumed_Rationale", 45, align_left),
        ("Evaluation_Set_and_Panel", 28, align_center)
    ]

    def populate_sheet(ws, dataset, title):
        # Header Row
        for col_idx, (col_name, col_width, _) in enumerate(columns, 1):
            cell = ws.cell(row=1, column=col_idx, value=col_name.replace("_", " "))
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = thin_border
            ws.column_dimensions[get_column_letter(col_idx)].width = col_width

        ws.row_dimensions[1].height = 28
        ws.freeze_panes = "C2" # Freeze Pair ID and Is Contradiction columns

        # Data Rows
        block_to_set = {
            "Block_1": "Set A (Panel A: SP-ANN-01 to 03)",
            "Block_2": "Set B (Panel B: SP-ANN-04 to 06)",
            "Block_3": "Set C (Panel C: SP-ANN-07 to 09)",
            "Block_4": "Set D (Panel D: SP-ANN-10 to 12)",
            "Block_5": "Set E (Panel E: SP-ANN-13 to 15)",
        }

        for row_idx, p in enumerate(dataset, 2):
            label = p["presumed_gold_label"]
            is_contra = "YES - CONTRADICTION" if label == "Contradiction" else "No (Entailment)" if label == "Entailment" else "No (Neutral)"
            
            # Extract short mechanism
            rat = p["presumed_rationale"]
            short_mech = rat.split(".")[0].replace("[District 1 (Poblacion/Talomo)] ", "").replace("[District 2 (Buhangin/Bunawan)] ", "").replace("[District 3 (Toril/Calinan/Marilog)] ", "").replace("[Domain 0 Evaluation Set] ", "")

            row_values = [
                p["pair_id"],
                is_contra,
                label,
                short_mech,
                p["difficulty_tier"],
                p["macro_domain_name"],
                p["national_premise"]["statute_title"],
                p["national_premise"]["citation"],
                p["national_premise"]["statutory_text"],
                p["ordinance_hypothesis"]["hypothesis_text"],
                p["ordinance_hypothesis"]["reference_context"],
                p["presumed_rationale"],
                block_to_set.get(p["block_id"], p["block_id"])
            ]

            ws.row_dimensions[row_idx].height = 65

            for col_idx, val in enumerate(row_values, 1):
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                cell.alignment = columns[col_idx-1][2]
                cell.border = thin_border
                cell.font = Font(name="Calibri", size=10)

                # Color badges
                if col_idx == 2 or col_idx == 3:
                    if label == "Contradiction":
                        cell.fill = fill_contra_badge
                        cell.font = font_contra_badge
                    elif label == "Entailment":
                        cell.fill = fill_entail_badge
                        cell.font = font_entail_badge
                    else:
                        cell.fill = fill_neutral_badge
                        cell.font = font_neutral_badge

    # 1. Sheet 1: Master 350 Pairs
    ws1 = wb.create_sheet(title="Master 350 Pairs Review")
    populate_sheet(ws1, pairs, "Master 350 Pairs Review")

    # 2. Sheet 2: Contradictions Only
    contradictions = [p for p in pairs if p["presumed_gold_label"] == "Contradiction"]
    ws2 = wb.create_sheet(title="Contradictions Only (116)")
    populate_sheet(ws2, contradictions, "Contradictions Only (116)")

    # 3. Sheet 3: Summary Matrix
    ws3 = wb.create_sheet(title="Domain & Tier Summary")
    ws3.column_dimensions['A'].width = 8
    ws3.column_dimensions['B'].width = 42
    ws3.column_dimensions['C'].width = 16
    ws3.column_dimensions['D'].width = 16
    ws3.column_dimensions['E'].width = 16
    ws3.column_dimensions['F'].width = 16

    # Summary Title
    title_cell = ws3.cell(row=1, column=1, value="GROUND TRUTH BENCHMARK (350 PAIRS) STRATIFICATION SUMMARY")
    title_cell.font = Font(name="Calibri", size=14, bold=True, color="1F497D")
    
    headers_summary = ["Domain ID", "Consolidated Macro Domain", "Contradiction", "Entailment", "Neutral", "Total Pairs"]
    for c_idx, h in enumerate(headers_summary, 1):
        cell = ws3.cell(row=3, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border

    from collections import defaultdict
    matrix = defaultdict(lambda: defaultdict(int))
    for p in pairs:
        matrix[p["macro_domain_id"]][p["presumed_gold_label"]] += 1

    dom_names = {
        0: "Executive Issuances & Policy Reorganization",
        1: "Education & Academic Institutions",
        2: "Local Government & Territorial Boundaries",
        3: "Public Utilities & Telecom Franchises",
        4: "Public Health, Hospitals & Medical Services",
        5: "Statutory Codes & General Legal Amendments",
        6: "Public Finance & General Appropriations",
        7: "Taxation, Tariffs & Revenue Administration"
    }

    current_row = 4
    for dom_id in range(8):
        c_cnt = matrix[dom_id]["Contradiction"]
        e_cnt = matrix[dom_id]["Entailment"]
        n_cnt = matrix[dom_id]["Neutral"]
        tot = c_cnt + e_cnt + n_cnt

        ws3.cell(row=current_row, column=1, value=f"{dom_id:02d}").alignment = align_center
        ws3.cell(row=current_row, column=2, value=dom_names[dom_id]).alignment = align_left
        ws3.cell(row=current_row, column=3, value=c_cnt).alignment = align_center
        ws3.cell(row=current_row, column=4, value=e_cnt).alignment = align_center
        ws3.cell(row=current_row, column=5, value=n_cnt).alignment = align_center
        ws3.cell(row=current_row, column=6, value=tot).alignment = align_center

        for c_idx in range(1, 7):
            ws3.cell(row=current_row, column=c_idx).border = thin_border
            ws3.cell(row=current_row, column=c_idx).font = Font(name="Calibri", size=11)
        current_row += 1

    # Total Row
    total_row = current_row
    ws3.cell(row=total_row, column=1, value="TOTAL").alignment = align_center
    ws3.cell(row=total_row, column=2, value="All 8 Macro Legal Domains").alignment = align_left
    ws3.cell(row=total_row, column=3, value=sum(matrix[d]["Contradiction"] for d in range(8))).alignment = align_center
    ws3.cell(row=total_row, column=4, value=sum(matrix[d]["Entailment"] for d in range(8))).alignment = align_center
    ws3.cell(row=total_row, column=5, value=sum(matrix[d]["Neutral"] for d in range(8))).alignment = align_center
    ws3.cell(row=total_row, column=6, value=len(pairs)).alignment = align_center

    for c_idx in range(1, 7):
        cell = ws3.cell(row=total_row, column=c_idx)
        cell.font = Font(name="Calibri", size=11, bold=True)
        cell.fill = fill_subhead
        cell.border = thin_border

    # 4. Sheet 4: Panel & Annotator Assignments
    ws4 = wb.create_sheet(title="Panel & Annotator Assignments")
    ws4.column_dimensions['A'].width = 16
    ws4.column_dimensions['B'].width = 14
    ws4.column_dimensions['C'].width = 20
    ws4.column_dimensions['D'].width = 16
    ws4.column_dimensions['E'].width = 36
    ws4.column_dimensions['F'].width = 18
    ws4.column_dimensions['G'].width = 32
    ws4.column_dimensions['H'].width = 28

    # Sheet Title
    t_cell = ws4.cell(row=1, column=1, value="SANGGUNIANG PANLUNGSOD (SP) ANNOTATION WORKLOAD & GOOGLE FORM DEPLOYMENT MATRIX")
    t_cell.font = Font(name="Calibri", size=14, bold=True, color="1F497D")
    sub_cell = ws4.cell(row=2, column=1, value="Master Roster for 350-Pair Ground Truth Benchmark (5 Sets, 5 Sub-Panels, 15 Legal Researchers, k=3 Overlap)")
    sub_cell.font = Font(name="Calibri", size=11, italic=True, color="595959")

    # Table 1: Sub-Panel Block Mapping
    sec1_title = ws4.cell(row=4, column=1, value="TABLE 1: UNIFIED EVALUATION SET & SUB-PANEL ALLOCATION")
    sec1_title.font = Font(name="Calibri", size=11, bold=True, color="1F497D")

    headers_blocks = [
        "Evaluation Set", "Sub-Panel", "Pair ID Range", "Pairs / Person", 
        "Assigned Annotator IDs (3 Raters)", "Total Ratings (k=3)", 
        "Single Master Form Section", "Source Pre-Split CSV"
    ]
    for c_idx, h in enumerate(headers_blocks, 1):
        cell = ws4.cell(row=5, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
    ws4.row_dimensions[5].height = 28

    panel_info = [
        ("Set A (Block 1)", "Panel A", "GT-001 to GT-070", 70, "SP-ANN-01, SP-ANN-02, SP-ANN-03", 210, "Section 2: Set A (Pairs 1-70)", "data/blocks/block_1.csv"),
        ("Set B (Block 2)", "Panel B", "GT-071 to GT-140", 70, "SP-ANN-04, SP-ANN-05, SP-ANN-06", 210, "Section 3: Set B (Pairs 71-140)", "data/blocks/block_2.csv"),
        ("Set C (Block 3)", "Panel C", "GT-141 to GT-210", 70, "SP-ANN-07, SP-ANN-08, SP-ANN-09", 210, "Section 4: Set C (Pairs 141-210)", "data/blocks/block_3.csv"),
        ("Set D (Block 4)", "Panel D", "GT-211 to GT-280", 70, "SP-ANN-10, SP-ANN-11, SP-ANN-12", 210, "Section 5: Set D (Pairs 211-280)", "data/blocks/block_4.csv"),
        ("Set E (Block 5)", "Panel E", "GT-281 to GT-350", 70, "SP-ANN-13, SP-ANN-14, SP-ANN-15", 210, "Section 6: Set E (Pairs 281-350)", "data/blocks/block_5.csv")
    ]

    for r_idx, row_data in enumerate(panel_info, 6):
        ws4.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row_data, 1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = thin_border
            cell.alignment = align_center if c_idx in [1, 2, 3, 4, 6] else align_left

    # Table 1 Total Row
    ws4.row_dimensions[11].height = 24
    tot_vals_1 = ["TOTAL", "5 Panels", "350 Unique Pairs", "70 Pairs / Person", "15 Legal Researchers", 1050, "1 Unified Master Form", "5 CSV Files Ready"]
    for c_idx, val in enumerate(tot_vals_1, 1):
        cell = ws4.cell(row=11, column=c_idx, value=val)
        cell.font = Font(name="Calibri", size=10, bold=True)
        cell.fill = fill_subhead
        cell.border = thin_border
        cell.alignment = align_center if c_idx in [1, 2, 3, 4, 6] else align_left

    # Table 2: Individual Annotator Directory
    ws4.cell(row=13, column=1, value="TABLE 2: INDIVIDUAL ANNOTATOR DIRECTORY (15 SANGGUNIANG PANLUNGSOD RESEARCHERS)").font = Font(name="Calibri", size=11, bold=True, color="1F497D")

    headers_ann = [
        "Annotator ID", "Evaluation Set", "Assigned Panel", "Assigned Pair Range", 
        "Workload (Pairs)", "Institutional Recruitment Pool", 
        "Professional Role & Designation", "Single Form Section Branch"
    ]
    for c_idx, h in enumerate(headers_ann, 1):
        cell = ws4.cell(row=14, column=c_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
    ws4.row_dimensions[14].height = 28

    annotators_list = [
        ("SP-ANN-01", "Set A", "Panel A", "GT-001 to GT-070", 70, "SP Legal Pool (Open Recruitment / First Available)", "Lead Legal Researcher (Senior: >= 5 Yrs SP Service)", "Branches to Section 2 (Set A)"),
        ("SP-ANN-02", "Set A", "Panel A", "GT-001 to GT-070", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Mid-Level)", "Branches to Section 2 (Set A)"),
        ("SP-ANN-03", "Set A", "Panel A", "GT-001 to GT-070", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Junior)", "Branches to Section 2 (Set A)"),
        ("SP-ANN-04", "Set B", "Panel B", "GT-071 to GT-140", 70, "SP Legal Pool (Open Recruitment / First Available)", "Lead Legal Researcher (Senior: >= 5 Yrs SP Service)", "Branches to Section 3 (Set B)"),
        ("SP-ANN-05", "Set B", "Panel B", "GT-071 to GT-140", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Mid-Level)", "Branches to Section 3 (Set B)"),
        ("SP-ANN-06", "Set B", "Panel B", "GT-071 to GT-140", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Junior)", "Branches to Section 3 (Set B)"),
        ("SP-ANN-07", "Set C", "Panel C", "GT-141 to GT-210", 70, "SP Legal Pool (Open Recruitment / First Available)", "Lead Legal Researcher (Senior: >= 5 Yrs SP Service)", "Branches to Section 4 (Set C)"),
        ("SP-ANN-08", "Set C", "Panel C", "GT-141 to GT-210", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Mid-Level)", "Branches to Section 4 (Set C)"),
        ("SP-ANN-09", "Set C", "Panel C", "GT-141 to GT-210", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Junior)", "Branches to Section 4 (Set C)"),
        ("SP-ANN-10", "Set D", "Panel D", "GT-211 to GT-280", 70, "SP Legal Pool (Open Recruitment / First Available)", "Lead Legal Researcher (Senior: >= 5 Yrs SP Service)", "Branches to Section 5 (Set D)"),
        ("SP-ANN-11", "Set D", "Panel D", "GT-211 to GT-280", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Mid-Level)", "Branches to Section 5 (Set D)"),
        ("SP-ANN-12", "Set D", "Panel D", "GT-211 to GT-280", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Junior)", "Branches to Section 5 (Set D)"),
        ("SP-ANN-13", "Set E", "Panel E", "GT-281 to GT-350", 70, "SP Legal Pool (Open Recruitment / First Available)", "Lead Legal Researcher (Senior: >= 5 Yrs SP Service)", "Branches to Section 6 (Set E)"),
        ("SP-ANN-14", "Set E", "Panel E", "GT-281 to GT-350", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Mid-Level)", "Branches to Section 6 (Set E)"),
        ("SP-ANN-15", "Set E", "Panel E", "GT-281 to GT-350", 70, "SP Legal Pool (Open Recruitment / First Available)", "Associate Legal Researcher (Junior)", "Branches to Section 6 (Set E)"),
    ]

    for r_idx, a_data in enumerate(annotators_list, 15):
        ws4.row_dimensions[r_idx].height = 20
        for c_idx, val in enumerate(a_data, 1):
            cell = ws4.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Calibri", size=10)
            cell.border = thin_border
            cell.alignment = align_center if c_idx in [1, 2, 3, 4, 5] else align_left

    # Table 3: Google Forms Setup Guidelines
    ws4.cell(row=31, column=1, value="TABLE 3: HOW TO BUILD ONE SINGLE GOOGLE FORM WITH CONDITIONAL BRANCHING").font = Font(name="Calibri", size=11, bold=True, color="1F497D")

    instructions = [
        ("Architecture Overview", "You can create EXACTLY ONE Google Form for all 15 annotators by utilizing Google Forms' native 'Go to section based on answer' (conditional branching) feature."),
        ("Purposive Sampling Logic", "Recruitment gathers the first 15 consenting legal researchers from the 48-member SP pool based on availability. Rigid district quotas are NOT enforced because all municipal ordinances govern the city as a whole. The sole structural requirement is ensuring each 3-person sub-panel has 1 Senior Lead (>= 5 years service)."),
        ("Section 1: Rater Identification", "Create Section 1 with a required dropdown: 'Select your Annotator ID' (options SP-ANN-01 to SP-ANN-15). In question settings (3 dots), check 'Go to section based on answer'."),
        ("Branching Configuration", "Route IDs: SP-ANN-01, 02, 03 -> Go to Section 2 (Set A) | SP-ANN-04, 05, 06 -> Go to Section 3 (Set B) | SP-ANN-07, 08, 09 -> Go to Section 4 (Set C) | SP-ANN-10, 11, 12 -> Go to Section 5 (Set D) | SP-ANN-13, 14, 15 -> Go to Section 6 (Set E)."),
        ("Crucial Navigation Step!", "At the bottom of each Section 2, 3, 4, and 5: change the default 'Continue to next section' to 'SUBMIT FORM'. This guarantees that each annotator submits after their 70 pairs and does NOT see subsequent sets."),
        ("Senior Annotator Metric", "Seniority is determined by years of active legal research service at the SP (>= 5 years). Each sub-panel has 1 Senior Lead and 2 Associates. All 3 evaluate independently/blind on the initial pass to prevent authority bias. Senior Adjudicator resolves 1-1-1 ties."),
        ("Item Presentation Layout", "Each item displays: (1) Pair ID & Statute Citation, (2) National Premise (Lawphil), (3) Local Ordinance Hypothesis (Draft). Inputs: Q1: Decision (Radio), Q2: Confidence (1-5), Q3: Notes (Text)."),
        ("Single Link Distribution", "Advantage: You distribute ONLY ONE link to the SP office. Every researcher selects their ID and gets routed automatically to their assigned 70 items, with all 1,050 responses aggregating into a single Google Sheet!")
    ]

    for r_idx, (step_title, step_desc) in enumerate(instructions, 32):
        ws4.row_dimensions[r_idx].height = 24
        c1 = ws4.cell(row=r_idx, column=1, value=step_title)
        c1.font = Font(name="Calibri", size=10, bold=True, color="1F497D")
        c1.border = thin_border
        c1.alignment = align_left

        # Merge columns B through H for description
        ws4.merge_cells(start_row=r_idx, start_column=2, end_row=r_idx, end_column=8)
        c2 = ws4.cell(row=r_idx, column=2, value=step_desc)
        c2.font = Font(name="Calibri", size=10)
        c2.border = thin_border
        c2.alignment = align_left
        for col_i in range(3, 9):
            ws4.cell(row=r_idx, column=col_i).border = thin_border

    # Save workbook
    try:
        wb.save(EXCEL_PATH)
        target_saved = EXCEL_PATH
    except PermissionError:
        fallback_path = os.path.join(ROOT_DIR, "data", "ground_truth_350_review_v4.xlsx")
        wb.save(fallback_path)
        target_saved = fallback_path
        print(f"Notice: '{EXCEL_PATH}' is currently open in Excel. Saved updated workbook to: {fallback_path}")

    # Also save to v4 as duplicate to ensure both files are fresh
    v4_path = os.path.join(ROOT_DIR, "data", "ground_truth_350_review_v4.xlsx")
    try:
        wb.save(v4_path)
    except Exception:
        pass

    print(f"SUCCESS! Excel workbook saved to: {target_saved} ({os.path.getsize(target_saved):,} bytes)")

if __name__ == "__main__":
    build_excel_review()
