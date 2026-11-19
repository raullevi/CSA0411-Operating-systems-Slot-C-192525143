#!/usr/bin/env python3
"""
Generates the comprehensive submission report DOCX for CSA0411 OS Assignment 3 (CO3)
Student: Rakul K | Register Number: 192525143
"""
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = parse_xml(f'<w:{m} {nsdecls("w")} w:w="{val}" w:type="dxa"/>')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(4)
    run = h.runs[0]
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 58, 138)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(51, 65, 85)
    return h

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Courier New"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(15, 23, 42)

def build_docx(filename="CSA0411_OS_Assignment3_CO3_Report_192525143.docx"):
    doc = docx.Document()

    # Page Margins (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Title Banner
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(2)
    r_uni = p_title.add_run("SIMATS ENGINEERING\nSAVEETHA INSTITUTE OF MEDICAL AND TECHNICAL SCIENCES\n")
    r_uni.font.name = "Arial"
    r_uni.font.size = Pt(12)
    r_uni.font.bold = True
    r_uni.font.color.rgb = RGBColor(71, 85, 105)

    r_course = p_title.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n")
    r_course.font.name = "Arial"
    r_course.font.size = Pt(11)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(100, 116, 139)

    r_sub = p_title.add_run("CSA0411 — OPERATING SYSTEMS (SLOT C)\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(15)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(15, 23, 42)

    r_ass = p_title.add_run("ASSIGNMENT 3 — COURSE OUTCOME 3 (CO3)\n")
    r_ass.font.name = "Arial"
    r_ass.font.size = Pt(13)
    r_ass.font.bold = True
    r_ass.font.color.rgb = RGBColor(37, 99, 235)

    r_meta = p_title.add_run("Bloom's Taxonomy Level: K5 - Evaluate | Total Marks: 50\n")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    # Metadata Table
    tbl = doc.add_table(rows=5, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta = [
        ("Student Name:", "Rakul K"),
        ("Register Number:", "192525143"),
        ("Course Faculty / Slot:", "CSA0411 (Slot C) — Operating Systems"),
        ("GitHub Repository Link:", "https://github.com/raullevi/CSA0411-Operating-systems-Slot-C-192525143.git"),
        ("Compiler / Environment:", "Apple Clang 21.0 / GCC 13+ (-std=c11 -Wall -Wextra -pthread -O2) on Darwin/Linux")
    ]
    for i, (k, v) in enumerate(meta):
        c0 = tbl.cell(i, 0)
        c1 = tbl.cell(i, 1)
        c0.text = k
        c1.text = v
        c0.paragraphs[0].runs[0].font.bold = True
        c0.paragraphs[0].runs[0].font.size = Pt(9.5)
        c1.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Question Distribution Matrix
    add_heading_styled(doc, "Assignment Mark Distribution & Syllabus Mapping", 2)
    tbl_dist = doc.add_table(rows=8, cols=4)
    tbl_dist.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Task", "Topic Area", "Cognitive Level", "Max Marks"]
    for j, h in enumerate(headers):
        cell = tbl_dist.cell(0, j)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E2E8F0")
    
    dist_rows = [
        ("Q1", "Linking, Loading and Address Binding", "K5 - Evaluate", "6 Marks"),
        ("Q2", "Paging (Address Translation & Complete the Code)", "K5 - Evaluate", "8 Marks"),
        ("Q3", "Segmentation, Protection and Shared Pages", "K5 - Evaluate", "6 Marks"),
        ("Q4", "Virtual Memory and Demand Paging", "K5 - Evaluate", "8 Marks"),
        ("Q5", "Page-Replacement Techniques (Complete the Code)", "K5 - Evaluate", "8 Marks"),
        ("Q6", "Disk Management & RAID Reliability", "K5 - Evaluate", "4 Marks"),
        ("Q7", "Memory-Management Plan from First Principles", "K5 - Evaluate", "10 Marks"),
    ]
    for i, r in enumerate(dist_rows):
        for j, val in enumerate(r):
            cell = tbl_dist.cell(i+1, j)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(9)
            set_cell_background(cell, "FFFFFF" if i % 2 == 0 else "F8FAFC")
            set_cell_margins(cell, 50, 50, 80, 80)

    doc.add_page_break()

    # ------------------ QUESTION 1 ------------------
    add_heading_styled(doc, "Q1: Linking, Loading and Address Binding (6 Marks)", 1)
    doc.add_paragraph("Problem Context: Updating a Banking Application\nA bank's branch software is built from many modules and libraries. When a security fix is made to the encryption library, every branch must currently receive a new 200 MB executable.")
    
    add_heading_styled(doc, "1. Implementation Tasks & Results", 2)
    doc.add_paragraph("We built both static and dynamic versions of the banking application and tested dynamic runtime loading via dlopen() and dlsym():")
    add_code_block(doc, """Artifact Comparison:
- bank_app_static  : 4.1 MB (Monolithic binary; embeds 4 MB encryption payload)
- bank_app_dynamic : 34 KB   (Tiny executable; links against @rpath/libencrypt.dylib)
- libencrypt.dylib : 4.0 MB  (Independent shared object)
- bank_app_dlopen  : 33 KB   (Loads library dynamically at runtime on demand)""")

    doc.add_paragraph("Zero-Recompile Hot Patching Verification:")
    add_code_block(doc, """1. Initial state with libencrypt_v1:
   Active Security Module: v1.0.0-LEGACY (VULNERABLE: Weak XOR Cipher, CVE-2026-BANK-01)
   Security Patch Status : CRITICAL RISK (UNPATCHED)

2. Replace shared object: cp libencrypt_v2.dylib libencrypt.dylib
3. Re-run bank_app_dynamic WITHOUT recompiling:
   Active Security Module: v2.1.0-PATCHED (SECURE: ChaCha20-Poly1305 / AES-256-GCM Compliance)
   Security Patch Status : SECURE (PATCHED)""")

    add_heading_styled(doc, "2. Theoretical Evaluation", 2)
    doc.add_paragraph("• Compile-time vs Load-time vs Execution-time Address Binding: Compile-time generates absolute addresses (recompile mandatory if location changes); Load-time generates relocatable offsets bound at exec time; Execution-time delays binding until instruction fetch via MMU base/limit registers.\n• Role of Linker vs Loader: The linker resolves external symbols, merges object sections, and performs relocations. The loader maps segments into virtual memory, initializes data/BSS, and jumps to entry point.\n• Position-Independent Code (PIC): Compiled with -fPIC using relative addressing via the Global Offset Table (GOT) and Procedure Linkage Table (PLT).")

    add_heading_styled(doc, "3. Conclusion & Recommendation", 2)
    doc.add_paragraph("Recommendation: The bank should transition to Dynamic Linking with versioned shared libraries. Replacing a 4 MB shared library instead of distributing a 200 MB monolithic executable saves 99% network bandwidth and allows immediate zero-recompile security hot-patching.")

    add_heading_styled(doc, "4. Alternative Concept & Complexity Analysis", 2)
    doc.add_paragraph("If the bank loads the encryption library at runtime with dlopen() only when needed:\n- Startup Time: O(1) instantaneous launch since the dynamic linker skips crypto symbol resolution at boot.\n- Memory Use: 0 MB memory overhead when teller terminals perform non-cryptographic balance inquiries.\n- Error Handling: dlopen() returns NULL and dlerror() provides error strings, enabling graceful offline fallback rather than abnormal process termination.")

    # ------------------ QUESTION 2 ------------------
    add_heading_styled(doc, "Q2: Paging (8 Marks)", 1)
    doc.add_paragraph("Problem Context: Memory for a Multi-User College Server\nA college server runs hundreds of student programs of very different sizes. Allocating each program one contiguous block of memory left many small unusable gaps (external fragmentation), and large programs could not be loaded although enough total memory was free.")

    add_heading_styled(doc, "1. Complete the Code Verification", 2)
    doc.add_paragraph("Completed TODO 1 in paging_todo.c matching the exact expected output for PAGE_SIZE = 1024:")
    add_code_block(doc, """0 -> page 0 offset 0 : physical 5120
1500 -> page 1 offset 476 : physical 2524
3100 -> page 3 offset 28 : physical 7196
6200 -> page 6 offset 56 : physical 3128
9000 -> page 8 offset 808 : invalid address
2049 -> page 2 offset 1 : page fault""")

    doc.add_paragraph("Recalculation by hand for PAGE_SIZE = 2048:")
    add_code_block(doc, """0 -> page 0 offset 0 : physical 10240
1500 -> page 0 offset 1500 : physical 11740
3100 -> page 1 offset 1052 : physical 5148
6200 -> page 3 offset 56 : physical 14392
9000 -> page 4 offset 808 : physical 808
2049 -> page 1 offset 1 : physical 4097""")

    add_heading_styled(doc, "2. Page Table Calculations & EMAT", 2)
    doc.add_paragraph("• 32-bit Address Space (4 KB pages): 2^20 pages * 4 bytes = 4 MB per process.\n• 48-bit Address Space (4 KB pages): 2^36 pages * 8 bytes = 512 GB per process! (Proves multi-level paging is required).\n• Effective Memory Access Time (EMAT) with t_mem = 100 ns, t_tlb = 10 ns:\n  - Without TLB: 2 * 100 ns = 200.0 ns\n  - TLB Hit Rate 80%: 0.80*(110) + 0.20*(210) = 130.0 ns (1.54x speedup)\n  - TLB Hit Rate 95%: 0.95*(110) + 0.05*(210) = 115.0 ns (1.74x speedup)\n  - TLB Hit Rate 99%: 0.99*(110) + 0.01*(210) = 111.0 ns (1.80x speedup)")

    add_heading_styled(doc, "3. 100-Process Fragmentation Simulation Results", 2)
    doc.add_paragraph("• 1 KB Page Size: 0.16% internal fragmentation waste (0.45 KB avg/proc).\n• 4 KB Page Size: 0.72% internal fragmentation waste (2.08 KB avg/proc) — Optimal Industry Balance.\n• 2 MB Huge Pages: 86.05% memory wasted in internal fragmentation for small student programs!")

    # ------------------ QUESTION 3 ------------------
    add_heading_styled(doc, "Q3: Segmentation (6 Marks)", 1)
    doc.add_paragraph("Problem Context: Student Programs with Separate Code, Stack, and Data\nStudents' programs have code that should be read-only and shared by everyone running the same compiler, a stack that grows, and data of varying size. Paging alone treats all of these the same.")

    add_heading_styled(doc, "1. Address Translation & SIGSEGV Exception Handling", 2)
    doc.add_paragraph("Verified 8 address translations in segmentation_sim.c:")
    add_code_block(doc, """[1] (0, 50)   Code Fetch          -> VALID: Base 1400 + Offset 50 = 1450
[2] (0, 1050) Code Buffer Overrun -> REJECTED: Offset 1050 >= Limit 1000 [SIGSEGV]
[3] (1, 200)  Data Global Read    -> VALID: Base 6300 + Offset 200 = 6500
[4] (1, 400)  Data Off-by-one     -> REJECTED: Offset 400 >= Limit 400 [SIGSEGV]
[5] (2, 150)  Stack Push          -> VALID: Base 4300 + Offset 150 = 4450
[6] (3, 720)  Shared Lib Call     -> VALID: Base 3200 + Offset 720 = 3920
[7] (4, 300)  Heap Malloc Read    -> VALID: Base 8500 + Offset 300 = 8800
[8] (5, 50)   Invalid Segment 5   -> REJECTED: Invalid Segment Selector""")

    doc.add_paragraph("OS Kernel Exception Action: When hardware MMU traps illegal pointer dereference (0x0), CPU escalates privilege from Ring 3 to Ring 0, constructs siginfo_t, and dispatches SIGSEGV to the process.")

    add_heading_styled(doc, "2. External Fragmentation Simulation", 2)
    doc.add_paragraph("After allocating and removing 20 segments across 1 MB physical RAM, 550 KB total RAM was free (53.7% free) across 11 disjoint holes. However, an incoming 150 KB job FAILED due to 81.09% external fragmentation! This proves why modern OSes rely on paging.")

    # ------------------ QUESTION 4 ------------------
    add_heading_styled(doc, "Q4: Virtual Memory and Demand Paging (8 Marks)", 1)
    doc.add_paragraph("Problem Context: Running Large Medical-Imaging Software on a Laptop\nA radiologist needs to run an image-processing program that uses 24 GB of memory on a laptop with 16 GB of RAM.")

    add_heading_styled(doc, "1. Effective Access Time (EAT) Math Calculations", 2)
    doc.add_paragraph("Formula: EAT = (1 - p) * 100 ns + p * 8,000,000 ns = 100 + p * 7,999,900 ns\n• p = 1 in 1,000 (0.1%): EAT = 8,099.9 ns (81.0x slower!)\n• p = 1 in 100,000 (0.001%): EAT = 180.0 ns (1.80x slower)\n• p = 1 in 1,000,000 (0.0001%): EAT = 108.0 ns (8% slowdown)\n• Maximum acceptable fault rate for <= 10% slowdown: p <= 1.25 * 10^-6 (At most 1 page fault in 800,000 accesses).")

    add_heading_styled(doc, "2. Experimental Verification", 2)
    doc.add_paragraph("• Copy-on-Write (COW): fork() completed instantaneously with 0 initial duplicate pages (Child RSS = 1,152 KB). Only upon writing was a single COW fault recorded.\n• Working Set Model: Plotted page faults against frame count (page_fault_curve.svg), showing working set knee at 10 frames where faults drop sharply from 36 down to 10.\n• Recommendation: Radiologist should optimize cache-blocking/tiling algorithms first, backed by a 32 GB RAM upgrade for concurrent multi-scan analysis.")

    # ------------------ QUESTION 5 ------------------
    add_heading_styled(doc, "Q5: Page-Replacement Techniques (8 Marks)", 1)
    doc.add_paragraph("Problem Context: Choosing a Policy for a Web Server\nA web server keeps frequently used pages of data in memory. When memory is full, the OS must choose which page to remove, and a poor choice causes slow responses.")

    add_heading_styled(doc, "1. Complete the Code Verification", 2)
    add_code_block(doc, """3 frames: FIFO 15, LRU 12, Optimal 9
4 frames: FIFO 10, LRU 8, Optimal 8
Belady string, FIFO: 3 frames 9 faults, 4 frames 10 faults""")

    doc.add_paragraph("Bélády's Anomaly Explanation: FIFO evicts purely by arrival time, so expanding frames changes queue alignments and evicts hot pages right before reuse. LRU is immune because it satisfies the Stack Property: B(t, n) is a strict subset of B(t, n+1).")

    add_heading_styled(doc, "2. 100,000 References Benchmark", 2)
    doc.add_paragraph("• FIFO: 55,036 faults (55.04% miss rate, 0.88 ms)\n• LRU: 51,574 faults (51.57% miss rate, 1.15 ms)\n• Clock (Second-Chance): 53,453 faults (53.45% miss rate, 1.57 ms)\n• Engineering Decision: Recommended the Clock algorithm. Clock comes within 1.8% of exact LRU fault rate while requiring only a single reference bit per PTE without timestamp bus contention.")

    # ------------------ QUESTION 6 ------------------
    add_heading_styled(doc, "Q6: Disk Management (4 Marks)", 1)
    doc.add_paragraph("Problem Context: Storage for a Hospital Records Server\nThe hospital records server must start reliably, survive the failure of a disk, and have enough swap space for peak load.")

    add_heading_styled(doc, "1. RAID Architecture & Reliability Model (6 Disks of 4 TB)", 2)
    doc.add_paragraph("• RAID 0: 24 TB usable (100%), 0 tolerance, 1x write penalty.\n• RAID 1: 12 TB usable (50%), survives 1 disk/pair, 2x write penalty.\n• RAID 5: 20 TB usable (83.3%), survives 1 disk, 4x write penalty.\n• RAID 6: 16 TB usable (66.7%), survives 2 disks, 6x write penalty.\n• RAID 10: 12 TB usable (50%), survives up to 3 disks, 2x write penalty.")

    doc.add_paragraph("Data Loss Probability during 24-hr Rebuild (AFR = 2%):\n• RAID 1: 0.00011% (1 in 912,500)\n• RAID 5: 0.00329% (1 in 30,416) — 30x higher risk of data loss than RAID 1!\n• Recommendation: RAID 10 on NVMe SSDs with a dedicated mirrored swap partition.")

    # ------------------ QUESTION 7 ------------------
    add_heading_styled(doc, "Q7: Memory-Management Plan from First Principles (10 Marks)", 1)
    doc.add_paragraph("Problem Context: Memory Management for an Edge Device in a Smart Factory\nEdge device with 2 GB RAM and NO swap disk. Runs a Real-Time control task (must NEVER be delayed by a page fault), a Machine Learning task (1.5 GB), a Logging task, and future tasks.")

    add_heading_styled(doc, "1. The 4-Stage Architectural Plan", 2)
    doc.add_paragraph("• Stage 1 (Problem Interpretation): Identified constraints: RT task (128 MB, 0 page faults, <50 us latency); ML task (1,536 MB, soft deadline); Logging (64 MB); OS Reserved (128 MB). Total budget = 1,856 MB / 2,048 MB (192 MB safety headroom).\n• Stage 2 (Candidate Comparison): Selected Paged Virtual Memory with mlockall(MCL_CURRENT | MCL_FUTURE) and stack pre-faulting for RT control task, paired with Linux cgroups v2 memory limit for ML task.\n• Stage 3 (Implementation & Verification): rt_memory_lock_benchmark.c demonstrated 0 page faults and deterministic sub-microsecond latency. System simulation confirmed 0 deadline misses across 10,000 cycles.\n• Stage 4 (Defending the Design & 4th Task Analysis): Adding a 500 MB task causes a 308 MB deficit, triggering the Linux OOM killer! Two mitigation options engineered:\n  1. zram compressed in-memory swap (+307 MB physical RAM gain).\n  2. Model Quantization (FP32 -> INT8), reducing ML model from 1.5 GB to 384 MB (liberating 1,152 MB of RAM).")

    doc.add_paragraph("Alternative Concept (RTOS vs Linux with mlock): Flat-memory RTOS gives microsecond determinism but lacks virtual memory and deep learning runtime frameworks. Linux with locked paging offers the ideal balance.")

    doc.save(filename)
    print(f"Generated comprehensive report document: {filename}")

if __name__ == '__main__':
    build_docx()
