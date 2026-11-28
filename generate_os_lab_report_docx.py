#!/usr/bin/env python3
"""
generate_os_lab_report_docx.py - Generates a comprehensive academic Word document (.docx)
for all 40 Operating Systems Laboratory Experiments (CSA04 / CSA0411).
"""

import os
import re
import glob
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

REPO_ROOT = "/Users/raul_levi/.gemini/antigravity/scratch/CSA0411-Operating-systems-Slot-C-192525143"
LAB_DIR = os.path.join(REPO_ROOT, "Lab Experiments")

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def parse_readme(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        text = f.read()

    title = ""
    m_title = re.search(r'^#\s+Experiment\s+\d+:\s*(.+)$', text, re.MULTILINE)
    if m_title:
        title = m_title.group(1).strip()

    co = "CO1"
    m_co = re.search(r'\*\*Course Outcome:\*\*\s*(CO\d+)', text)
    if m_co:
        co = m_co.group(1).strip()

    aim = ""
    m_aim = re.search(r'##\s*AIM\s*\n(.*?)(?=\n##\s*)', text, re.DOTALL)
    if m_aim:
        aim = m_aim.group(1).strip()

    procedure = ""
    m_proc = re.search(r'##\s*PROCEDURE\s*\n(.*?)(?=\n##\s*)', text, re.DOTALL)
    if m_proc:
        procedure = m_proc.group(1).strip()

    return title, co, aim, procedure

def create_os_lab_report():
    print("Scanning OS Lab Experiments (Exp01 - Exp40)...")
    exp_dirs = sorted(glob.glob(os.path.join(LAB_DIR, "Exp[0-9][0-9]_*")))
    print(f"Found {len(exp_dirs)} experiment directories.")

    experiments = []
    for d in exp_dirs:
        dirname = os.path.basename(d)
        m_num = re.match(r'^Exp(\d+)_', dirname)
        exp_num = int(m_num.group(1)) if m_num else 0

        readme_path = os.path.join(d, "README.md")
        title, co, aim, procedure = parse_readme(readme_path)
        if not title:
            title = dirname

        # Source file (main.c or script.sh)
        c_path = os.path.join(d, "main.c")
        sh_path = os.path.join(d, "script.sh")
        if os.path.exists(c_path):
            src_name = "main.c"
            with open(c_path, "r", encoding="utf-8") as f:
                src_code = f.read()
        elif os.path.exists(sh_path):
            src_name = "script.sh"
            with open(sh_path, "r", encoding="utf-8") as f:
                src_code = f.read()
        else:
            src_name = "N/A"
            src_code = ""

        input_path = os.path.join(d, "input.txt")
        input_txt = ""
        if os.path.exists(input_path):
            with open(input_path, "r", encoding="utf-8") as f:
                input_txt = f.read().strip()

        output_path = os.path.join(d, "output.txt")
        output_txt = ""
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                output_txt = f.read().strip()

        png_path = os.path.join(d, f"exp{exp_num:02d}_output.png")
        if not os.path.exists(png_path):
            png_candidates = glob.glob(os.path.join(d, "*.png"))
            png_path = png_candidates[0] if png_candidates else ""

        experiments.append({
            "num": exp_num,
            "dirname": dirname,
            "title": title,
            "co": co,
            "aim": aim,
            "procedure": procedure,
            "src_name": src_name,
            "src_code": src_code,
            "input_txt": input_txt,
            "output_txt": output_txt,
            "png_path": png_path,
        })

    doc = Document()
    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Title Page
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run(
        "\n\nSAVEETHA SCHOOL OF ENGINEERING\n"
        "SAVEETHA INSTITUTE OF MEDICAL AND TECHNICAL SCIENCES (SIMATS)\n"
    )
    r_inst.bold = True
    r_inst.font.size = Pt(16)
    r_inst.font.color.rgb = RGBColor(0, 51, 102)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n\n\n")
    r_dept.bold = True
    r_dept.font.size = Pt(13)
    r_dept.font.color.rgb = RGBColor(90, 90, 90)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run(
        "CSA04 / CSA0411 - OPERATING SYSTEMS\n"
        "LABORATORY RECORD (EXPERIMENTS 01 TO 40)\n\n\n"
    )
    r_title.bold = True
    r_title.font.size = Pt(20)
    r_title.font.color.rgb = RGBColor(0, 51, 102)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run(
        "STUDENT NAME: RAKUL K\n"
        "REGISTER NUMBER: 192525143\n"
        "SLOT: SLOT C\n"
        "DEGREE: B.TECH (COMPUTER SCIENCE & ENGINEERING)\n"
        "ACADEMIC YEAR: 2026 - 2027\n"
    )
    r_meta.bold = True
    r_meta.font.size = Pt(12)

    doc.add_page_break()

    # Index Table
    doc.add_heading("Index of Operating Systems Lab Experiments", level=1)
    toc_table = doc.add_table(rows=1, cols=4)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = toc_table.rows[0].cells
    hdr[0].text = "Exp #"
    hdr[1].text = "CO"
    hdr[2].text = "Experiment Title"
    hdr[3].text = "Source File"
    for cell in hdr:
        set_cell_background(cell, "003366")
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(9.5)

    for exp in experiments:
        row = toc_table.add_row().cells
        row[0].text = f"{exp['num']:02d}"
        row[1].text = exp["co"]
        row[2].text = exp["title"]
        row[3].text = exp["src_name"]
        for cell in row:
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.size = Pt(9)

    doc.add_page_break()

    # Each Experiment Section
    for exp in experiments:
        doc.add_heading(f"Experiment {exp['num']:02d}: {exp['title']}", level=1)

        meta_table = doc.add_table(rows=2, cols=2)
        meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        meta_table.rows[0].cells[0].text = "Course: CSA04 / CSA0411 - Operating Systems"
        meta_table.rows[0].cells[1].text = "Student: Rakul K (192525143)"
        meta_table.rows[1].cells[0].text = f"Course Outcome: {exp['co']}"
        meta_table.rows[1].cells[1].text = f"Source File: {exp['src_name']} (Verified)"
        for r in meta_table.rows:
            for c in r.cells:
                set_cell_background(c, "F0F4F8")
                for p in c.paragraphs:
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        run.font.size = Pt(9.5)

        if exp["aim"]:
            doc.add_heading("1. Aim", level=2)
            p_aim = doc.add_paragraph(exp["aim"])
            p_aim.paragraph_format.space_after = Pt(4)

        if exp["procedure"]:
            doc.add_heading("2. Procedure / Algorithm", level=2)
            p_proc = doc.add_paragraph(exp["procedure"])
            p_proc.paragraph_format.space_after = Pt(4)

        doc.add_heading(f"3. Source Code ({exp['src_name']})", level=2)
        p_code = doc.add_paragraph()
        r_code = p_code.add_run(exp["src_code"])
        r_code.font.name = "Courier New"
        r_code.font.size = Pt(8.5)
        p_code.paragraph_format.space_after = Pt(4)

        if exp["input_txt"]:
            doc.add_heading("4. Sample Input (input.txt)", level=2)
            p_in = doc.add_paragraph()
            r_in = p_in.add_run(exp["input_txt"])
            r_in.font.name = "Courier New"
            r_in.font.size = Pt(8.5)
            p_in.paragraph_format.space_after = Pt(4)

        doc.add_heading("5. Execution Output (output.txt)", level=2)
        p_out = doc.add_paragraph()
        r_out = p_out.add_run(exp["output_txt"])
        r_out.font.name = "Courier New"
        r_out.font.size = Pt(8.5)
        p_out.paragraph_format.space_after = Pt(4)

        if exp["png_path"] and os.path.exists(exp["png_path"]):
            doc.add_heading("6. Terminal Output Screenshot", level=2)
            doc.add_picture(exp["png_path"], width=Inches(6.2))

        doc.add_page_break()

    out_root = os.path.join(REPO_ROOT, "CSA0411_OS_Lab_Report_40_Experiments.docx")
    out_lab = os.path.join(LAB_DIR, "CSA0411_OS_Lab_Report_40_Experiments.docx")
    out_dl = "/Users/raul_levi/Downloads/CSA0411_OS_Lab_Report_40_Experiments.docx"

    doc.save(out_root)
    shutil.copyfile(out_root, out_lab)
    shutil.copyfile(out_root, out_dl)
    print(f"Saved OS Lab Report to:\n  - {out_root}\n  - {out_lab}\n  - {out_dl}")

if __name__ == "__main__":
    create_os_lab_report()
