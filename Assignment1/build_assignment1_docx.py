#!/usr/bin/env python3
"""
build_assignment1_docx.py
Generates the comprehensive, official submission Word (.docx) document
for CSA0411 / CSA04 Assignment 1 (CO1) for Rakul K (192525143).
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

    # Title & Header
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

    r_title = p_dept.add_run("OPERATING SYSTEMS (CSA0411 / CSA04) - SLOT C\nASSIGNMENT 1 - COURSE OUTCOME 1 (CO1)\nEVALUATE AND JUSTIFY THE OPERATING-SYSTEM DESIGN OF A SMART HOSPITAL")
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
        ("GitHub Repository Link:", "https://github.com/raullevi/CSA04-192525143-Assignment1.git")
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
    h = doc.add_heading("TASK 1 – Evaluate Requirements of Each Computing Environment (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "A 500-bed hospital requires specialized operating systems across six environments: bedside patient monitors "
        "(alarm <= 10ms), nurses' handheld tablets, doctors' workstations, central database server, MRI imaging server, "
        "and links to partner hospitals."
    )
    add_callout(doc,
        "RANKED REQUIREMENTS & CONFLICT RESOLUTION:\n"
        "• Bedside Monitors: Deterministic latency (<= 10ms) is life-critical (Rank 1). General-purpose time-sharing schedulers "
        "conflict with real-time determinism by introducing unbounded dispatch delays.\n"
        "• Nurses' Tablets: Battery longevity (> 12h shift) conflicts with unconstrained background syncing; resolved via cgroups and power scaling.\n"
        "• Central Database: 99.999% availability with zero downtime (< 3s failover) prioritized over raw unbuffered speed.",
        "TASK 1 EVALUATION (K5)"
    )

    # TASK 2
    h = doc.add_heading("TASK 2 – Judge the Type of Operating System for Each Environment (3 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Bedside Monitors: Hard Real-Time OS (QNX / FreeRTOS) – provides bounded interrupt latency.\n"
        "• Nurses' Tablets: Handheld Mobile OS (Hardened Android AOSP) – mobile power management and touch UI.\n"
        "• Doctors' Workstations: Desktop OS (Ubuntu LTS) – interactive multitasking and PACS DICOM peripherals.\n"
        "• Database Server: Clustered OS with High-Availability Failover (Pacemaker/Corosync) – eliminates single point of failure.\n"
        "• MRI Imaging Server: Symmetric Multiprocessing (SMP) Linux – 92% parallel scaling across 32 cores (superior to AMP)."
    )
    add_callout(doc,
        "ALTERNATIVE ANALYSIS (SINGLE SMP NODE VS CLUSTER):\n"
        "A single large SMP mainframe node creates a catastrophic Single Point of Failure (SPOF). Hardware crashes cause 15-minute "
        "blackouts halting emergency surgeries. A 2-node cluster provides automatic heartbeat failover in < 3 seconds.",
        "TASK 2 EVALUATION (K5)"
    )

    # TASK 3
    h = doc.add_heading("TASK 3 – Evaluate Operating-System Structures (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Bedside Monitors: Microkernel Structure (seL4 / QNX). Drivers run in isolated Ring 3 user space. A crash in an SpO2 sensor "
        "driver restarts in < 5ms without taking down cardiac alarms.\n"
        "• Database Server: Modular Monolithic Linux. Storage and networking run in Ring 0 for high IOPS throughput, with dynamic kernel modules (LKMs) for SAN drivers."
    )

    # TASK 4
    h = doc.add_heading("TASK 4 – Evaluate the Services an Operating System Must Provide (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Service Pruning for Monitors: Removed shells, demand paging/swap, desktop GUI managers, and dynamic package tools. "
        "Retained hardware watchdog timers, ADC sensor drivers, and UDP telemetry streaming to minimize attack surface and memory footprint.\n"
        "• Protection: Hardware MMU/MPU sandboxing isolates patient ECG buffers from external network packets."
    )

    # TASK 5
    h = doc.add_heading("TASK 5 – Examine System Calls (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Anatomy of read(): Glibc loads fd in RDI, buffer in RSI, count in RDX, and 0 in RAX. The 'syscall' instruction causes hardware "
        "mode switch from User Mode (Ring 3) to Kernel Mode (Ring 0). Kernel validates pointers, reads page cache, copies data, and executes 'sysretq'.\n"
        "Buffering via fread() reduces syscall count by 99.97% compared to 1-byte raw read() calls."
    )

    # TASK 6
    h = doc.add_heading("TASK 6 – Evaluate the Cost of System Calls (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph("Completed code for TODO 1 in `Task06_Cost_of_System_Calls/copy_file_todo.c`:")
    add_code_block(doc, """// Completed TODO 1 (Loop read and write):
while (1) {
    calls++;
    n = read(in, buf, bufsize);
    if (n <= 0) break;
    if (write(out, buf, n) != n) {
        close(in);
        close(out);
        return -1;
    }
}""")
    doc.add_paragraph("Execution Output (Exact Match with Specification):")
    add_code_block(doc, """buffer    1 bytes: 10001 read() calls
buffer  512 bytes:    21 read() calls
buffer 4096 bytes:     4 read() calls""")

    ss6 = os.path.join(OUTPUT_SS_DIR, "task06_output_screenshot.png")
    if os.path.exists(ss6):
        doc.add_picture(ss6, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 1: Task 06 Terminal Execution Output (copy_file buffer study)").font.size = Pt(8.5)

    # TASK 7
    h = doc.add_heading("TASK 7 – Evaluate Process Control System Calls (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph("Completed code for TODO 1 in `Task07_Process_Control/shell_todo.c`:")
    add_code_block(doc, """// Completed TODO 1 (fork, execlp, waitpid):
pid_t pid1 = fork();
if (pid1 < 0) {
    perror("fork failed");
    exit(1);
} else if (pid1 == 0) {
    execlp("expr", "expr", "6", "*", "7", (char *)NULL);
    exit(127);
} else {
    int status1;
    waitpid(pid1, &status1, 0);
    printf("job 1 exit status %d\\n", WEXITSTATUS(status1));
}""")
    doc.add_paragraph("Execution Output (Exact Match with Specification):")
    add_code_block(doc, """shell: running job 1
42
job 1 exit status 0
shell: running job 2
job 2 exit status 3""")

    ss7 = os.path.join(OUTPUT_SS_DIR, "task07_output_screenshot.png")
    if os.path.exists(ss7):
        doc.add_picture(ss7, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 2: Task 07 Terminal Execution Output (shell job runner)").font.size = Pt(8.5)

    add_callout(doc,
        "STDLIB BUFFER FLUSHING ANALYSIS:\n"
        "stdout is block-buffered when redirected to files. If fflush(stdout) is omitted before fork(), the child process inherits "
        "the parent's unflushed user-space buffer. When both parent and child exit, both flush the buffer, causing 'shell: running job 2' "
        "to be output TWICE. Flushing before fork() guarantees clean buffer state.",
        "TASK 7 EVALUATION (K5)"
    )

    # TASK 8
    h = doc.add_heading("TASK 8 – Evaluate CPU States and Protection (3 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Dual Mode Operation: Hardware mode bit enforces Ring 3 user restrictions. Timer interrupts preempt runaway loops to ensure "
        "patient alarms fire within 10ms.\n"
        "• Interrupt Disabling: The CLI instruction is privileged. If user apps could disable interrupts, sensor interrupts would be masked, "
        "causing fatal silent failure during cardiac arrest.\n"
        "• Polling vs Interrupts: Polling consumes 100% CPU and introduces 50ms latency; interrupts wake CPU in < 2µs from sleep state."
    )

    # TASK 9
    h = doc.add_heading("TASK 9 – Evaluate the Memory Hierarchy and I/O Systems (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Storage Hierarchy: Registers (< 0.5ns) -> Caches (1-10ns) -> RAM (50-100ns) -> NVMe SSD (15µs) -> HDD (8ms) -> Cloud S3 (80ms).\n"
        "• DMA for MRI Scans: Bus-master DMA streams 500MB MRI images across PCIe directly into RAM in 17.8ms with 1 interrupt, "
        "whereas programmed I/O would consume 125 Million CPU interrupts, freezing doctor workstations for over 2 minutes."
    )

    # TASK 10
    h = doc.add_heading("TASK 10 – Measure and Compare (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph("Microbenchmark Results (1,000 Processes vs 1,000 Threads):")
    ss10 = os.path.join(OUTPUT_SS_DIR, "task10_output_screenshot.png")
    if os.path.exists(ss10):
        doc.add_picture(ss10, width=Inches(6.2))
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run("Figure 3: Task 10 Benchmark Output (1,000 Processes vs 1,000 Threads)").font.size = Pt(8.5)

    add_callout(doc,
        "BENCHMARK EVALUATION:\n"
        "• 1,000 Processes: 0.8345 s (834.52 µs / process).\n"
        "• 1,000 Threads: 0.0170 s (16.99 µs / thread) -> 49.1x Faster!\n"
        "Threads share virtual memory page tables and file handles, whereas processes require full page-table duplication. "
        "This empirical proof validates rejecting process-per-session in hospital systems.",
        "TASK 10 EVALUATION (K5)"
    )

    # TASK 11
    h = doc.add_heading("TASK 11 – Recommend and Defend the Operating-System Plan (4 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "• Bedside Monitors: QNX/FreeRTOS Microkernel (deterministic 10ms SLA, MPU sandbox).\n"
        "• Nurses' Tablets: Hardened Android AOSP (14-hour battery, touch UI).\n"
        "• Doctors' Workstations: Ubuntu Desktop Linux (multitasking, PACS DICOM viewing).\n"
        "• Central Database Server: 2-Node Active/Passive Linux Cluster (99.999% uptime, < 3s failover).\n"
        "• MRI Imaging Server: 128-core SMP Linux with CUDA/DMA for parallel volumetric reconstruction.\n"
        "• Scaling to 3 Hospitals: Local edge autonomy + central streaming read-replicas across dedicated encrypted leased lines."
    )

    # TASK 12
    h = doc.add_heading("TASK 12 – Day-4 Design Challenge: Re-evaluate and Adapt (8 Marks)", level=1)
    h.runs[0].font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph(
        "Changed Requirement: Home wearable patient monitoring over public internet + Cloud-based patient records.\n"
        "• Part A (Impact Analysis): Public internet has high jitter; cloud migration shifts database to managed cloud services.\n"
        "• Part B (Evaluation of Original Design): Original design lacked internet transport resilience; on-premise servers cannot handle 150,000 cloud users.\n"
        "• Part C (Adaptation): Modified into a Hybrid Edge-Cloud Architecture. Home wearables run Zephyr RTOS with localized ML anomaly "
        "detection (local audible siren in < 5ms). Cloud records migrate to Amazon EKS / Google Cloud with Aurora PostgreSQL.\n"
        "• Part D (Defense): Guarantees life-safety during home internet outages while enabling infinite elastic scale in the cloud."
    )

    doc.save(out_path)
    print(f"Successfully generated Assignment 1 document at: {out_path}")

if __name__ == "__main__":
    out1 = "/Users/raul_levi/Downloads/Rakul_K_192525143_CSA0411_Assignment1_Answers.docx"
    out2 = "/Users/raul_levi/Downloads/Rakul_K_192525143_CSA04_Assignment1_Answers.docx"
    build_docx(out1)
    build_docx(out2)
