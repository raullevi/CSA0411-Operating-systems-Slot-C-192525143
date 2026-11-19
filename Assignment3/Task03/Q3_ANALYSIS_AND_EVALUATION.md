# Q3: Segmentation — Evaluation, Implementation & Analysis

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Segmentation, Segment Tables, Fragmentation, Protection (K5 - Evaluate, 6 Marks)  

---

## 1. Problem Context — Student Programs with Separate Code, Stack, and Data
Students' programs naturally consist of logically distinct modules:
- **Code (Text):** Instructions that should be strictly read-only and shared across all students running the same compiler or library.
- **Data (Globals/BSS):** Variable-sized data structures that require read and write permissions.
- **Stack:** Dynamically growing structure that expands downward during recursive function calls.
- **Heap:** Dynamically allocated heap memory growing upward via `malloc()`.

### The Core Problem:
Pure paging treats memory as flat, fixed-sized, anonymous chunks (e.g., 4 KB blocks) with zero semantic relationship to program structure. In pure paging:
- A single page might accidentally cross the boundary between read-only code and writable global data.
- Enforcing fine-grained protection and sharing requires artificial page padding.
- Segmentation matches the **programmer's mental model** by viewing memory as a collection of variable-length logical units.

---

## 2. Address Translation & Segment Table Architecture

### 2.1 Segment Translation Logic
A logical address is represented as a 2-tuple: `(segment_number, offset)`.
1. The CPU checks if `segment_number` is within the bounds of the Segment Table:
   $$\text{If } s \ge \text{Segment\_Table\_Length} \implies \mathbf{Trap: Invalid\ Segment\ Selector}$$
2. The hardware compares `offset` with `Limit`:
   $$\text{If } d \ge \text{Limit}[s] \implies \mathbf{Trap: Addressing\ Beyond\ Limit\ (SIGSEGV)}$$
3. If valid, the physical address is computed by:
   $$\text{Physical Address} = \text{Base}[s] + d$$

```
Logical Address: [ Segment Selector s | Offset d ]
                            |               |
               +------------+               |
               |                            |
               v                            v
        [ Segment Table ]            +--------------+
        | Base  | Limit |            |  d < Limit?  | --(No)--> [ TRAP: SIGSEGV ]
        +-------+-------+            +--------------+
        | Base0 | Lim0  |                   | (Yes)
        | Base1 | Lim1  |                   v
        | ...   | ...   | ---------> [ Base + d ] ====> [ PHYSICAL MEMORY ]
```

---

## 3. Hand Calculation of 8 Test Addresses (Verified via Program)

Given Segment Table:
- **Seg 0 (Code):** Base = 1400, Limit = 1000 (R-X)
- **Seg 1 (Data):** Base = 6300, Limit = 400 (RW-)
- **Seg 2 (Stack):** Base = 4300, Limit = 500 (RW-)
- **Seg 3 (Shared Lib):** Base = 3200, Limit = 1500 (R-X)
- **Seg 4 (Heap):** Base = 8500, Limit = 600 (RW-)

| # | Logical Address $(s, d)$ | Description | Validation Check | Result / Physical Address |
|---|---|---|---|---|
| 1 | **(0, 50)** | Instruction fetch from Code | $50 < 1000$ (Valid) | $\text{Physical} = 1400 + 50 = \mathbf{1450}$ |
| 2 | **(0, 1050)** | Buffer overrun in Code | $1050 \ge 1000$ (Violation) | $\mathbf{TRAP: Offset \ge Limit\ [SIGSEGV]}$ |
| 3 | **(1, 200)** | Global variable read | $200 < 400$ (Valid) | $\text{Physical} = 6300 + 200 = \mathbf{6500}$ |
| 4 | **(1, 400)** | Boundary off-by-one error | $400 \ge 400$ (Violation) | $\mathbf{TRAP: Offset \ge Limit\ [SIGSEGV]}$ |
| 5 | **(2, 150)** | Stack push activation record | $150 < 500$ (Valid) | $\text{Physical} = 4300 + 150 = \mathbf{4450}$ |
| 6 | **(3, 720)** | Shared compiler library call | $720 < 1500$ (Valid) | $\text{Physical} = 3200 + 720 = \mathbf{3920}$ |
| 7 | **(4, 300)** | Malloc heap block access | $300 < 600$ (Valid) | $\text{Physical} = 8500 + 300 = \mathbf{8800}$ |
| 8 | **(5, 50)** | Access non-existent segment | $s = 5 \ge 5$ (Out of bounds) | $\mathbf{TRAP: Invalid\ Segment\ Selector}$ |

*All 8 calculations verified programmatically in `segmentation_sim.c`.*

---

## 4. Triggering Hardware SIGSEGV & OS Kernel Exception Handling

When our test code executed `*(volatile int *)0x0 = 0xDEADBEEF;`:
1. **Hardware MMU Exception:** The memory management unit encountered an unmapped segment selector/page translation fault.
2. **Privilege Escalation:** CPU hardware immediately suspended the user thread, saved instruction pointer and register context, and switched from **User Mode (Ring 3)** to **Kernel Mode (Ring 0)**.
3. **Trap Handler Execution:** The Linux/XNU kernel page fault handler checked the memory descriptor (`vm_area_struct` / segment descriptor). Finding no valid write permission, it constructed a `siginfo_t` packet with code `SEGV_MAPERR` / `SEGV_ACCERR`.
4. **Signal Dispatch:** Kernel delivered `SIGSEGV` (Signal 11). Our registered signal handler caught the trap, recorded the faulting address `0x0`, and restored control via `longjmp()`. Without this handler, the OS terminates the process with `Segmentation fault (core dumped)`.

---

## 5. Segmented Paging (Intel x86 Architecture)

To combine the logical benefits of segmentation with the physical allocation advantages of paging, architectures like Intel x86 use **Segmentation with Paging**:

```
Logical Address: [ Selector | Offset ]
                         |
                         v
                [ Segment Descriptor ]  ---> Checked against Limit & Rights
                         |
                         +-------------> Base Address + Offset
                                                |
                                                v
                                        [ Linear Address ]
                                                |
                         +----------------------+----------------------+
                         |                      |                      |
                         v                      v                      v
                  [ Directory Index ]     [ Table Index ]          [ Offset ]
                         |                      |                      |
                         v                      v                      v
                  [ Page Directory ]    [ Page Table ]         [ Physical Frame ]
```
1. **Segmentation Unit:** Translates Logical Address into a continuous 32/64-bit **Linear Address**.
2. **Paging Unit:** Translates the Linear Address into a **Physical Address** using hierarchical page tables.

---

## 6. Experimental Fragmentation Analysis

From our empirical 20-segment simulation in `segmentation_sim.c`:
- **Total Physical Pool:** 1,024 KB (1 MB).
- **Total Free Memory Available:** 550 KB (**53.7% free**).
- **Number of Disjoint Holes:** 11 holes (checkerboard pattern).
- **Largest Single Contiguous Hole:** **104 KB**.
- **Incoming 150 KB Student Job Allocation:** **FAILED!**
- **Calculated External Fragmentation:** **81.09%**.

> **Evaluation:** Although over half of physical memory is completely free (550 KB), no segment of 150 KB can be loaded because the memory is shattered into small, non-contiguous holes. Overcoming this requires **costly compaction (shuffling memory)** or **paging**.

---

## 7. Comparative Architectural Evaluation

| Feature | Pure Paging | Pure Segmentation | Segmented Paging |
|---|---|---|---|
| **Programmer View** | Linear, contiguous flat address space | Logical modular view (code, stack, data) | Modular view mapped to flat linear space |
| **Block Size** | Fixed (e.g. 4 KB) | Variable (dependent on program modules) | Paged frames (4 KB) backing variable segments |
| **External Fragmentation** | **Zero** | **Severe (up to 80%+)** | **Zero** |
| **Internal Fragmentation** | Minor (average 1/2 page per segment) | **Zero** | Minor (in final page of each segment) |
| **Hardware Support Needed** | MMU Page Tables + TLB | Base and Limit Registers | Segment registers (GDT/LDT) + MMU Page Tables |
| **Table Size Overhead** | High (proportional to address space) | **Very Low** (5-16 segment descriptors) | Moderate (small segment table + paged tables) |
| **Sharing & Protection** | Coarse page-level bits | Fine-grained natural module boundaries | Fine-grained permissions per segment |

---

## 8. Conclusion
**Why do modern operating systems rely mainly on paging?**

Modern operating systems (Linux, macOS, Windows) rely primarily on **paging** (with a "flat" segmentation model where Segment Base = 0 and Limit = Max Address Space) because:
1. **Elimination of External Fragmentation:** Memory allocation requires simply popping free fixed frames from a bitmap/free list. No compaction or defragmentation is ever needed.
2. **Virtual Memory & Swapping Simplicity:** Fixed 4 KB frames make disk-to-memory swapping and demand paging highly deterministic and efficient for storage controllers.
3. **Compiler & Toolchain Simplification:** Compilers and linkers generate flat linear virtual addresses, avoiding complex 16-bit far pointers or segment register management.
4. **Module Protection via Page Attributes:** Modern OSes achieve segment-like protection by grouping virtual memory into VM areas (`vm_area_struct` in Linux) that enforce R/W/X protection bits on individual 4 KB pages.

---

## 9. Alternative Concept & Complexity Analysis
**Alternative Concept:** Pure Paging instead of Segmentation.

### 1. Fragmentation Comparison:
- **Segmentation:** Zero internal fragmentation, but high external fragmentation ($O(\text{holes})$). Requires memory compaction with $O(M)$ data copy overhead.
- **Pure Paging:** Zero external fragmentation. Internal fragmentation is bounded by at most $\frac{1}{2} \times \text{PAGE\_SIZE}$ per allocated region.

### 2. Table Memory Complexity:
- **Segment Table:** Space complexity is $O(S)$ where $S$ is the number of modules (typically $S \le 16$). Requires less than 256 bytes per process.
- **Page Table:** Space complexity is $O(V / \text{PAGE\_SIZE})$ where $V$ is the virtual address space. Requires hundreds of kilobytes to megabytes per process.

### 3. Translation Time Complexity:
- **Segmentation:** $O(1)$ single addition (`Base + Offset`) with one hardware limit comparison.
- **Paging:** $O(L)$ where $L$ is page table depth (4 memory accesses without TLB; $O(1)$ with TLB hit).
