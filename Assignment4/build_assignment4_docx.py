#!/usr/bin/env python3
"""
build_assignment4_docx.py
Generates the comprehensive, official submission Word (.docx) document
for CSA0411 / CSA04 Assignment 4 (CO4) for Rakul K (192525143).
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_SS_DIR = os.path.join(BASE_DIR, "output_ss")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="EVALUATION & DESIGN DECISION (K5)"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    c = tbl.cell(0, 0)
    set_cell_background(c, "F0F4F8")
    set_cell_margins(c, top=140, bottom=140, left=180, right=180)

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"[{title}]\n")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(16, 75, 142)

    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    c = tbl.cell(0, 0)
    set_cell_background(c, "1E293B")
    set_cell_margins(c, top=100, bottom=100, left=140, right=140)

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(241, 245, 249)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_docx(out_path):
    doc = docx.Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.75)
        sec.bottom_margin = Inches(0.75)
        sec.left_margin = Inches(0.75)
        sec.right_margin = Inches(0.75)

    # Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("SIMATS ENGINEERING\nSAVEETHA INSTITUTE OF MEDICAL AND TECHNICAL SCIENCES")
    r_inst.bold = True
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(14)
    r_inst.font.color.rgb = RGBColor(15, 23, 42)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n")
    r_dept.bold = True
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(11)
    r_dept.font.color.rgb = RGBColor(71, 85, 105)

    r_title = p_dept.add_run("OPERATING SYSTEMS (CSA0411 / CSA04) - SLOT C\nASSIGNMENT 4 - COURSE OUTCOME 4 (CO4)\nOPTIMISING FILE STORAGE AND DISK ACCESS")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(12)
    r_title.font.color.rgb = RGBColor(30, 64, 175)

    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(2.2)
    meta_table.columns[1].width = Inches(4.3)

    fields = [
        ("Student Name:", "Rakul K"),
        ("Register Number:", "192525143"),
        ("Course & Slot:", "CSA0411 / CSA04 - Operating Systems (Slot C)"),
        ("Bloom's Taxonomy Level:", "K5 – Evaluate (All Tasks Assessed at K5 Level)"),
        ("GitHub Repository Link:", "https://github.com/raullevi/CSA04-192525143-Assignment4.git")
    ]

    for idx, (lbl, val) in enumerate(fields):
        c0, c1 = meta_table.cell(idx, 0), meta_table.cell(idx, 1)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 50, 50, 80, 80)
        set_cell_margins(c1, 50, 50, 80, 80)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(lbl)
        r0.bold = True
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        if "github.com" in val:
            r1.bold = True
            r1.font.color.rgb = RGBColor(37, 99, 235)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # TASK 1
    h = doc.add_heading("TASK 1 – File-System Design Review (6 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "A college proposes storing files for 12,000 students on a shared server in a single flat directory with "
        "arbitrary student filenames, contiguous allocation, and zero access control."
    )
    add_callout(doc,
        "FIVE CRITICAL WEAKNESSES & REDESIGN:\n"
        "1. Namespace Collisions: Identical filenames (e.g. lab1.c) overwrite peer submissions.\n"
        "2. Linear Directory Lookup: O(N) search across 600,000 files causes severe latency.\n"
        "3. Contiguous Allocation Failure: Severe external fragmentation; growing files must be relocated.\n"
        "4. Security/Privacy Breach: Unrestricted access allows students to inspect, copy, or delete peers' exams.\n"
        "5. Backup/Recovery Impossibility: Cannot perform per-student incremental backups.\n\n"
        "DEFENDED REDESIGN (<= 100 WORDS):\n"
        "The hierarchical tree directory isolates student namespaces, preventing collisions and reducing search latency to O(log N). "
        "Strict POSIX permissions (750) and discretionary ACLs enforce mandatory confidentiality, ensuring students cannot inspect "
        "or modify peer files. Collaboration is enabled cleanly via SGID group project repositories linked into individual home directories "
        "using symbolic links. This dual structure guarantees privacy, supports dynamic file growth, and enables automated backups.",
        "TASK 1 EVALUATION & DEFENCE (K5)"
    )

    # TASK 2
    h = doc.add_heading("TASK 2 – Workload to File-Allocation Method (8 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Storage for Video-Surveillance Recorder (32 cameras, continuous growth, sequential playback, random seeks, 30-day deletion)."
    )
    doc.add_paragraph("Completed code for TODO 1 in `Task02_Workload_to_FileAllocation/file_alloc_todo.c`:")
    add_code_block(doc, """// Completed TODO 1 (First-Fit Contiguous Allocation):
int count = 0, start = -1;
for (int i = 0; i < BLOCKS; i++) {
    if (disk[i] == '.') {
        if (count == 0) start = i;
        count++;
        if (count == size) {
            for (int j = start; j < start + size; j++) {
                disk[j] = file;
            }
            return start;
        }
    } else {
        count = 0;
        start = -1;
    }
}
return -1;""")

    doc.add_paragraph("Execution Output (Exact Match with Specification):")
    add_code_block(doc, """AAAAAA........CCCCC.............
E (10 blocks) contiguous: start 19
E (10 blocks) indexed: index block 6, data blocks 7 8 9 10 11 12 13 29 30 31
AAAAAAeEEEEEEECCCCCEEEEEEEEEEEEE""")

    ss2 = os.path.join(OUTPUT_SS_DIR, "task02_output_screenshot.png")
    if os.path.exists(ss2):
        doc.add_picture(ss2, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 1: Task 02 Terminal Execution Output (File Allocation Sim)").font.size = Pt(8.5)

    add_callout(doc,
        "MATHEMATICAL CALCULATIONS (4 GB FILE WITH 4 KB BLOCKS = 1,048,576 BLOCKS):\n"
        "• Contiguous: 1 disk read (LBA = Start + 1,048,575).\n"
        "• Linked Allocation (pointers in data blocks): 1,048,576 disk reads.\n"
        "• Linked Allocation (in-memory FAT): 1 disk read (FAT traversed in RAM).\n"
        "• Indexed Allocation (Inode): 3 disk reads (double-indirect pointer -> index block -> data block).\n"
        "• Inode Max File Size: 12 Direct (48KB) + Single (4MB) + Double (4GB) + Triple (4TB) = ~4.004 TB.\n"
        "• Free-Space Bit Vector for 4 TB disk = 1,073,741,824 bits = 128 MB RAM.",
        "TASK 2 EVALUATION (K5)"
    )

    # TASK 3
    h = doc.add_heading("TASK 3 – Modern File Systems (9 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Comparison: ext4 (journaling), XFS (high-throughput parallel extent allocation), ZFS (end-to-end checksums, native CoW snapshots), "
        "APFS (flash-optimized CoW cloning).\n"
        "• Device Recommendations: Pen drive (exFAT/FAT32 for universal cross-platform); Linux database (XFS for parallel DIO); "
        "Laptop (APFS/ext4 for SSD power/encryption); Backup server (ZFS for self-healing bit-rot protection and instant snapshots).\n"
        "• Ext4 Journaling: data=journal (slowest, full payload logging); data=ordered (default, data written before metadata committed); "
        "data=writeback (fastest, metadata only, risks stale data exposure)."
    )

    # TASK 4
    h = doc.add_heading("TASK 4 – Disk Scheduling Algorithms (7 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph("Request Queue: {98, 183, 37, 122, 14, 124, 65, 67}, Head at 53 (Cylinders 0–199).")
    doc.add_paragraph("Completed code for TODO 1 in `Task04_Disk_Scheduling_Algorithms/disk_sched_todo.c`:")
    add_code_block(doc, """// Completed TODO 1 (SSTF Greedy Selection):
int best_idx = -1;
int min_dist = 999999;
for (int i = 0; i < N; i++) {
    if (!done[i]) {
        int dist = abs(req[i] - pos);
        if (dist < min_dist) {
            min_dist = dist;
            best_idx = i;
        }
    }
}
done[best_idx] = 1;
order[k] = req[best_idx];
pos = req[best_idx];""")

    doc.add_paragraph("Execution Output (Exact Match with Specification):")
    add_code_block(doc, """FCFS   53 98 183 37 122 14 124 65 67 -> 640 cylinders
SSTF   53 65 67 37 14 98 122 124 183 -> 236 cylinders
SCAN   53 37 14 0 65 67 98 122 124 183 -> 236 cylinders
C-SCAN 53 65 67 98 122 124 183 199, jump to 0 14 37 -> 183 cylinders (+199 for the jump)""")

    ss4 = os.path.join(OUTPUT_SS_DIR, "task04_output_screenshot.png")
    if os.path.exists(ss4):
        doc.add_picture(ss4, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 2: Task 04 Terminal Execution Output (Disk Scheduling Suite)").font.size = Pt(8.5)

    add_callout(doc,
        "STARVATION & SSD SCHEDULING EVALUATION:\n"
        "• SSTF Starvation: When continuous requests arrive near cylinder 60, request 183 is starved indefinitely.\n"
        "• C-SCAN Uniformity: Treats cylinders as circular ring, eliminating bias towards middle tracks and bounding waiting time.\n"
        "• Solid-State Drives (SSDs): Flash has zero mechanical head seek delay. Linux assigns 'none' or 'mq-deadline' to bypass "
        "elevator sorting and eliminate multi-core lock contention.",
        "TASK 4 EVALUATION (K5)"
    )

    # TASK 5
    h = doc.add_heading("TASK 5 – Distributed and Cloud-Based Storage (7 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Comparison: NFS (local LAN labs, single SPOF); Ceph/HDFS (3-way replication, strong consistency, scale-out research); "
        "Cloud S3 (11 9s durability, remote student submission archive).\n"
        "• CAP Theorem Trade-off: Strong consistency (Ceph) enforces quorum for grade ledgers; Eventual consistency (S3) optimizes video streaming availability.\n"
        "• Device Management: Buffering decouples bursts; Caching accelerates reads via RAM; Spooling serializes batch devices."
    )

    # TASK 6
    h = doc.add_heading("TASK 6 – Day-4 Design Challenge: Video-Streaming Start-up (13 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph("Storage architecture for 200,000 students streaming lecture videos (300MB to 2GB).")
    doc.add_paragraph("Simulation Output (`video_storage_sim`):")
    add_code_block(doc, """Benchmark Simulation Results:
Metric / Measurement           | Design A (HDD Only)   | Design B (Tiered NVMe + HDD)
Total Stream Requests Served   | 100000                | 100000               
NVMe Cache Hit Rate            | 0.00% (No SSD Cache)  | 80.12% (80/20 Rule Working)
Average Playback Start Latency |    8.50 ms             |    1.73 ms (Speedup: 4.9x)
Max Concurrent Streams / Server| ~120 streams (Head I/O)| ~8,500 streams (PCIe NVMe)""")

    ss6 = os.path.join(OUTPUT_SS_DIR, "task06_output_screenshot.png")
    if os.path.exists(ss6):
        doc.add_picture(ss6, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 3: Task 06 Terminal Output (Tiered Video Storage Simulation)").font.size = Pt(8.5)

    add_callout(doc,
        "DESIGN CHALLENGE DEFENSE & CALCULATIONS:\n"
        "• HLS Chunking: Videos split into 2-second fragments (1 MB). Starting playback at any minute requires exactly 2 disk reads (manifest + chunk).\n"
        "• Tiered NVMe/HDD Architecture: Hot week-1 videos cached on NVMe SSDs (80.12% hit rate) reduce seek latency from 8.5ms to 1.73ms (4.9x speedup) "
        "and boost server concurrency from 120 to 8,500 streams.\n"
        "• Pure Cloud CDN vs Hybrid: Pure cloud object storage incurs ~$500,000/month egress fees; Hybrid on-premise NVMe origin servers with "
        "Cloudflare edge caching provides maximum throughput at minimal cost.",
        "TASK 6 EVALUATION (K5)"
    )

    doc.save(out_path)
    print(f"Successfully generated Assignment 4 document at: {out_path}")

if __name__ == "__main__":
    out1 = "/Users/raul_levi/Downloads/Rakul_K_192525143_CSA0411_Assignment4_Answers.docx"
    out2 = "/Users/raul_levi/Downloads/Rakul_K_192525143_CSA04_Assignment4_Answers.docx"
    build_docx(out1)
    build_docx(out2)
