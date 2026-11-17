# Q2: Paging — Evaluation, Analysis & Complete the Code

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Paging, Address Translation, Page Tables (K5 - Evaluate, 8 Marks)  

---

## 1. Problem Context — Memory for a Multi-User College Server
A college server runs hundreds of student programs of widely varying sizes (from 2 KB simple C assignments to 50 MB data science scripts). 
- **The Contiguous Allocation Problem:** When processes were allocated contiguous blocks of physical memory, allocating and terminating jobs created severe **external fragmentation** (checkerboarding). Unusable free holes were scattered between active processes. 
- Even though the server had 12 GB of total free RAM in aggregate, a 50 MB program could not be loaded because no single contiguous hole of 50 MB existed!

```
Contiguous Allocation External Fragmentation:
+-------------------+----------+-------------------+----------+-------------------+
| Process A (20 MB) | Hole 5MB | Process B (40 MB) | Hole 8MB | Process C (15 MB) | ...
+-------------------+----------+-------------------+----------+-------------------+
Total free memory = 5MB + 8MB + ... = 100 MB, but a 20 MB request FAILS!
```

---

## 2. Complete the Code Verification

### 2.1 C Implementation (`paging_todo.c`)
The logical address is split into:
$$\text{Page Number } p = \lfloor a / \text{PAGE\_SIZE} \rfloor, \quad \text{Offset } d = a \pmod{\text{PAGE\_SIZE}}$$

```c
// Completed TODO 1 Logic:
unsigned p = a / page_size;
unsigned d = a % page_size;

if (p >= PAGES) {
    printf("invalid address\n");
} else if (page_table[p] == -1) {
    printf("page fault\n");
} else {
    unsigned frame = (unsigned)page_table[p];
    unsigned physical = frame * page_size + d;
    printf("physical %u\n", physical);
}
```

### 2.2 Execution Output Comparison
Given `page_table[8] = {5, 2, -1, 7, 0, -1, 3, -1}`:

#### Part 1: `PAGE_SIZE = 1024` (Prompt Default)
| Logical Address $a$ | Page $p$ | Offset $d$ | Frame (`page_table[p]`) | Status / Physical Address |
|---|---|---|---|---|
| **0** | $0 / 1024 = 0$ | $0$ | 5 | `physical 5120` ($5 \times 1024 + 0$) |
| **1500** | $1500 / 1024 = 1$ | $476$ | 2 | `physical 2524` ($2 \times 1024 + 476$) |
| **3100** | $3100 / 1024 = 3$ | $28$ | 7 | `physical 7196` ($7 \times 1024 + 28$) |
| **6200** | $6200 / 1024 = 6$ | $56$ | 3 | `physical 3128` ($3 \times 1024 + 56$) |
| **9000** | $9000 / 1024 = 8$ | $808$ | N/A ($p \ge 8$) | `invalid address` |
| **2049** | $2049 / 1024 = 2$ | $1$ | -1 | `page fault` |

*Exact match with expected output on Assignment Page 5.*

#### Part 2: Hand Recalculation for `PAGE_SIZE = 2048`
When the frame size doubles to 2048 bytes:
1. $a = 0 \implies p = 0 / 2048 = 0, d = 0 \implies \text{Frame } 5 \implies \text{Physical } = 5 \times 2048 + 0 = \mathbf{10240}$
2. $a = 1500 \implies p = 1500 / 2048 = 0, d = 1500 \implies \text{Frame } 5 \implies \text{Physical } = 5 \times 2048 + 1500 = \mathbf{11740}$
3. $a = 3100 \implies p = 3100 / 2048 = 1, d = 3100 - 2048 = 1052 \implies \text{Frame } 2 \implies \text{Physical } = 2 \times 2048 + 1052 = \mathbf{5148}$
4. $a = 6200 \implies p = 6200 / 2048 = 3, d = 6200 - 6144 = 56 \implies \text{Frame } 7 \implies \text{Physical } = 7 \times 2048 + 56 = \mathbf{14392}$
5. $a = 9000 \implies p = 9000 / 2048 = 4, d = 9000 - 8192 = 808 \implies \text{Frame } 0 \implies \text{Physical } = 0 \times 2048 + 808 = \mathbf{808}$
6. $a = 2049 \implies p = 2049 / 2048 = 1, d = 2049 - 2048 = 1 \implies \text{Frame } 2 \implies \text{Physical } = 2 \times 2048 + 1 = \mathbf{4097}$

> **Critical Evaluation:** With $PAGE\_SIZE=2048$, address 9000 is no longer invalid (it falls within page 4), and address 2049 no longer causes a page fault (it falls within page 1, frame 2). Larger page sizes reduce page table entries and page faults for sequentially dispersed addresses, but increase internal fragmentation.

---

## 3. Mathematical Calculations & Architectural Analysis

### 3.1 Page Table Size Calculations (4 KB Pages)
A 4 KB page requires $\log_2(4096) = 12$ offset bits.

#### Case A: 32-bit Address Space
- Virtual Address: 32 bits $\implies$ Page Number = $32 - 12 = 20$ bits.
- Number of Pages = $2^{20} = 1,048,576$ pages.
- Assuming 4 bytes per Page Table Entry (PTE):
  $$\text{Table Size} = 2^{20} \times 4\text{ bytes} = 4,194,304\text{ bytes} = \mathbf{4\text{ MB per process!}}$$
- For 100 student processes: $100 \times 4\text{ MB} = \mathbf{400\text{ MB}}$ allocated purely for page tables!

#### Case B: 48-bit Address Space (Modern x86-64 Architecture)
- Virtual Address: 48 bits $\implies$ Page Number = $48 - 12 = 36$ bits.
- Number of Pages = $2^{36} \approx 6.87 \times 10^{10}$ pages.
- Assuming 8 bytes per PTE (64-bit pointers + flags):
  $$\text{Flat Table Size} = 2^{36} \times 8\text{ bytes} = 2^{39}\text{ bytes} = \mathbf{512\text{ GB per process!}}$$
- **Evaluation:** A single flat page table would exceed the entire physical RAM of the server ($512\text{ GB} \gg 64\text{ GB}$). Hence, flat page tables are completely impossible on 64-bit architectures, making **Hierarchical (4-Level / 5-Level Paging)** mandatory.

---

### 3.2 Effective Memory Access Time (EMAT) Calculations
Given: $t_{\text{mem}} = 100\text{ ns}$, $t_{\text{TLB}} = 10\text{ ns}$.

$$\text{EMAT} = h \times (t_{\text{TLB}} + t_{\text{mem}}) + (1 - h) \times (t_{\text{TLB}} + 2 \times t_{\text{mem}})$$

1. **Without TLB:**
   Every access requires 1 page table lookup + 1 physical memory fetch:
   $$\text{EMAT}_{\text{No-TLB}} = 2 \times 100\text{ ns} = \mathbf{200.0\text{ ns}}$$

2. **With TLB:**
   - **For $h = 80\%$:**
     $$\text{EMAT} = 0.80 \times (10 + 100) + 0.20 \times (10 + 200) = 0.80(110) + 0.20(210) = 88 + 42 = \mathbf{130.0\text{ ns}} \quad (1.54\times \text{ faster})$$
   - **For $h = 95\%$:**
     $$\text{EMAT} = 0.95(110) + 0.05(210) = 104.5 + 10.5 = \mathbf{115.0\text{ ns}} \quad (1.74\times \text{ faster})$$
   - **For $h = 99\%$:**
     $$\text{EMAT} = 0.99(110) + 0.01(210) = 108.9 + 2.1 = \mathbf{111.0\text{ ns}} \quad (1.80\times \text{ faster})$$

---

## 4. Evaluation of Advanced Page Table Structures

```
Hierarchical (Multi-Level)          Inverted Page Table
         CR3 Register                    (PID, Virtual Page #)
              |                                     |
              v                                     v
       [ PML4 Table ]                        [ Hash Function ]
        /    |     \                                |
       v     v      v                               v
    [PDPT] [PDPT]  [PDPT]                    [ Hash Anchor Table ]
      |                                             |
      v                                             v
    [PD]                                   [ Frame Array in RAM ]
      |                                    +--------------------+
      v                                    | Frame 0: (PID 12, P1)
    [PT]                                   | Frame 1: (PID 44, P0)
      |                                    +--------------------+
      v                                    (Fixed size = Physical RAM / Page Size)
    [ Physical Frame ]
```

1. **Hierarchical (Multi-Level) Page Tables:**
   - Breaks the virtual address into multiple indices (e.g. PML4 $\to$ PDPT $\to$ PD $\to$ PT $\to$ Offset).
   - Only allocates tables for active address regions (sparse memory). Unmapped address ranges require 0 table memory.
2. **Hashed Page Tables:**
   - Common for address spaces $> 32$ bits. Hash of virtual page number indexes a bucket chain of PTEs.
3. **Inverted Page Tables:**
   - Contains exactly **one entry per physical memory frame** rather than one per virtual page.
   - Saves massive amounts of RAM because table size is proportional to physical memory, not the processes' virtual address spaces.

---

## 5. Experimental Investigation (100 Processes Simulation)

From empirical execution of `paging_sim.c` over 100 student workloads (1 KB to 512 KB):
```
Page Size                    Allocated RAM    Wasted (Frag)    Avg Frag/Proc    Wastage %    
----------------------------------------------------------------------------------------
1 KB (Small)                        27.94 MB         0.04 MB         0.45 KB         0.16%
4 KB (Standard Linux/POSIX)         28.10 MB         0.20 MB         2.08 KB         0.72%
2 MB (Huge Pages)                  200.00 MB       172.10 MB      1762.32 KB        86.05%
```

### Engineering Trade-Offs:
- **1 KB Pages:** Internal fragmentation is negligible (0.16%), but page table size quadruples and TLB reach is tiny, causing frequent TLB misses.
- **4 KB Pages:** Ideal balance between internal fragmentation (0.72% waste) and TLB efficiency.
- **2 MB Huge Pages:** Catastrophic for small student programs (86% memory wasted in internal fragmentation), but beneficial for large databases or ML models.

---

## 6. Conclusion
**What page size would you choose for the college server, and why?**

**Decision:** We choose **4 KB standard paging with Transparent Huge Pages (THP) support**.
1. Student processes are predominantly small CLI programs, compilers, and lab exercises. A 4 KB page limits internal fragmentation to less than 1% ($2.08\text{ KB}$ per process).
2. Modern CPUs (x86-64 and ARM64) feature high-speed L1/L2 TLBs tuned for 4 KB granules.
3. For large research tasks (e.g., student AI/ML neural networks), the OS automatically coalesces contiguous 4 KB pages into 2 MB huge pages on demand via THP, avoiding fragmentation for small jobs while boosting TLB performance for large jobs.

---

## 7. Alternative Concept & Complexity Analysis
**Alternative Concept:** An **Inverted Page Table (IPT)** with hash lookup instead of per-process multi-level page tables.

### 1. Space Complexity:
- **Multi-Level Page Table:** Space is $O(\sum_{i=1}^N V_i)$, proportional to the total virtual address space of all active processes.
- **Inverted Page Table:** Space is $O(M_{\text{phys}} / \text{PAGE\_SIZE})$, strictly bounded by physical RAM size regardless of how many processes exist!

### 2. Translation Time Complexity:
- **Multi-Level Page Table:** $O(L)$ where $L$ is the number of levels (e.g., $L=4$ in x86-64). Deterministic tree traversal.
- **Inverted Page Table:** $O(1)$ average hash table lookup, but worst-case $O(K)$ where $K$ is the length of hash collision chains. Furthermore, every memory reference requires hashing (PID, Page#), which adds CPU ALU overhead unless assisted by hardware inverted translation registers.
