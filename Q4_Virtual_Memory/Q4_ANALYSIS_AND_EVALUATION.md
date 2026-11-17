# Q4: Virtual Memory and Demand Paging — Evaluation & Analysis

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Virtual Memory, Demand Paging, Thrashing, Working-Set Model (K5 - Evaluate, 8 Marks)  

---

## 1. Problem Context — Medical-Imaging Software on a Laptop
A hospital radiologist needs to process high-resolution 3D volumetric CT/MRI scans using an image-processing suite requiring **24 GB of virtual address space**. However, the radiologist's hospital laptop has only **16 GB of physical RAM**.

### Key Questions:
1. How does demand paging allow a 24 GB application to execute on a 16 GB machine?
2. What are the performance penalties of page faulting, and what is the maximum fault rate tolerable for a 10% slowdown?
3. What is thrashing, and how does the operating system detect and prevent it?
4. Is purchasing extra physical RAM (32 GB) or optimizing algorithmic memory locality the superior engineering decision?

---

## 2. Demand Paging & The 6-Step Page Fault Handling Sequence

Demand paging brings pages into physical RAM only when they are referenced during execution (lazy loading).

```
Instruction (e.g. Load M)
       |
       v
+-------------+      Invalid Bit (0)
|     MMU     | ------------------------> [ 1. TRAP to OS Kernel ]
+-------------+                                    |
                                                   v
                                          [ 2. Save CPU Registers ]
                                                   |
                                                   v
                                          [ 3. Validate Address in VMA ]
                                                   |
                                          (If illegal -> SIGSEGV)
                                                   v
                                          [ 4. Find / Evict Free Frame ]
                                          (If victim dirty -> write to swap)
                                                   |
                                                   v
                                          [ 5. Disk I/O Read from Swap ]
                                                   |
                                                   v
                                          [ 6. Update PTE (Set Valid=1) ]
                                                   |
                                                   v
                                          [ Restart Instruction ]
```

1. **Hardware MMU Trap:** CPU references a virtual address whose Page Table Entry (PTE) has `Valid = 0`. MMU traps to OS.
2. **Context Save:** Kernel saves volatile CPU registers and process state.
3. **Legality Verification:** Kernel consults internal Virtual Memory Area (`vm_area_struct`) tables. If access is outside legal virtual bounds, a `SIGSEGV` is sent. If valid, it is a demand page fault.
4. **Frame Allocation & Victim Eviction:** Kernel allocates an empty frame. If physical RAM is full, the page replacement algorithm selects a victim frame. If dirty, the victim is written to backing swap disk.
5. **Disk I/O Service:** Disk controller reads the requested 4 KB page from swap/SSD into the selected physical frame. The process waits in I/O block state.
6. **PTE Update & Instruction Restart:** Kernel writes the frame number to the PTE, sets `Valid = 1`, clears dirty bit, restores CPU registers, and restarts the instruction that caused the trap.

---

## 3. Mathematical Calculations: Effective Access Time (EAT)

Given Parameters:
- Memory Access Time: $t_{\text{mem}} = 100\text{ ns}$
- Page Fault Service Time: $t_{\text{fault}} = 8\text{ ms} = 8,000,000\text{ ns}$
- Formula:
  $$\text{EAT} = (1 - p) \times t_{\text{mem}} + p \times t_{\text{fault}} = 100 + p \times 7,999,900\text{ ns}$$

### 3.1 Calculated EAT Matrix
| Page Fault Rate $p$ | Calculation ($100 + p \times 7,999,900$) | EAT (ns) | EAT ($\mu\text{s}$) | Slowdown vs Memory |
|---|---|---|---|---|
| **1 in 1,000 ($10^{-3}$)** | $100 + 7,999.9$ | **8,099.90 ns** | **8.10 $\mu\text{s}$** | **81.00$\times$ slower** |
| **1 in 100,000 ($10^{-5}$)** | $100 + 79.999$ | **180.00 ns** | **0.18 $\mu\text{s}$** | **1.80$\times$ slower (80% drop)** |
| **1 in 1,000,000 ($10^{-6}$)** | $100 + 7.9999$ | **108.00 ns** | **0.11 $\mu\text{s}$** | **1.08$\times$ slower (8% drop)** |

### 3.2 Maximum Acceptable Page-Fault Rate for $\le 10\%$ Slowdown
To restrict slowdown to $\le 10\%$:
$$\text{EAT} \le 1.10 \times 100\text{ ns} = 110\text{ ns}$$
$$100 + p \times 7,999,900 \le 110 \implies p \times 7,999,900 \le 10$$
$$p \le \frac{10}{7,999,900} \approx \mathbf{1.25 \times 10^{-6}} \quad (\mathbf{1\text{ page fault in every } 800,000\text{ memory accesses}})$$

> **Evaluation:** Because mechanical/SSD disk I/O ($8\text{ ms}$) is nearly **80,000 times slower** than RAM ($100\text{ ns}$), even a tiny fault rate ($0.1\%$) destroys execution throughput by $8100\%$. High access locality is paramount.

---

## 4. Copy-on-Write (COW) and Fast `fork()`
When a process invokes `fork()`:
- **Traditional UNIX:** Duplicates every physical memory page from parent to child ($O(N)$ data copy, wasting massive RAM and latency).
- **Copy-on-Write (COW):** Parent and child share the identical physical frames. Both processes mark their page table entries as **Read-Only**.
- When either process writes to a shared page, the MMU triggers a protection fault. The OS kernel traps the fault, allocates a single fresh physical frame, copies only that specific 4 KB page, updates the faulting process's PTE with write permissions, and resumes execution.
- **Experimental Verification (`vm_experiments.c`):** A 32 MB parent spawned a child with zero memory duplicate overhead (Child initial RSS: 1,152 KB). Only upon writing was a single COW fault triggered.

---

## 5. Thrashing & The Working-Set Model

```
   CPU
Utilization
    ^                  Optimal Degree of Multiprogramming
100%|                         /\
    |                        /  \
    |                       /    \
    |                      /      \  THRASHING COLLAPSE
    |                     /        \  (Paging disk saturated,
    |                    /          \  CPU utilization drops to ~0)
    +-------------------+------------+------------------------>
                        Degree of Multiprogramming (Processes)
```

### 5.1 Definition of Thrashing
Thrashing occurs when a system spends more time servicing page faults than executing instructions.
- If the sum of working sets exceeds available physical memory:
  $$\sum_{i=1}^N \text{WSS}_i > \text{Total Physical Frames}$$
  processes constantly evict each other's active pages, page fault queues saturate the storage controller, and CPU utilization plunges to near-zero.

### 5.2 Working-Set Model ($WSS$)
- Defined by Peter Denning: The **Working Set** $WSS_i(t, \Delta)$ is the set of pages referenced by process $i$ during the most recent window of $\Delta$ memory references.
- **OS Thrashing Prevention:**
  1. If $\sum \text{WSS}_i \le \text{Total Frames}$, all processes fit in memory.
  2. If $\sum \text{WSS}_i > \text{Total Frames}$, the OS suspends (swaps out) one or more lower-priority processes completely, liberating all their frames for active jobs.
  3. **Page-Fault Frequency (PFF):** Sets upper and lower thresholds on fault rates. If a process exceeds the upper threshold, it receives more frames; if it drops below the lower threshold, excess frames are reclaimed.

### 5.3 Frame Allocation Strategies
- **Equal Allocation:** Splits available frames equally ($m / n$). Unfair to memory-intensive processes like the 24 GB imaging application.
- **Proportional Allocation:** Allocates frames according to virtual size $s_i$:
  $$a_i = \frac{s_i}{\sum s_k} \times m$$

---

## 6. Experimental Curve: Page Faults vs Allocated Frames

From simulated 36-reference medical scan access string in `vm_experiments.c`:
```
Frames   Page Faults     Fault Rate (%)     Working Set Status
-----------------------------------------------------------------
1        36              100.00%            Catastrophic thrashing
3        33               91.67%            Severe thrashing
5        27               75.00%            High faulting
6        24               66.67%            Plateau region
9        24               66.67%            Plateau region
10       10               27.78%            Working Set Knee (Satisfied!)
```
*(Vector graph exported to `page_fault_curve.svg`)*.

---

## 7. Conclusion: Hardware Upgrade vs Algorithmic Locality
**Is buying more RAM (32 GB) or improving the program's locality the better solution for the radiologist?**

### Evaluation & Verdict:
**Recommendation: A Dual-Pronged Strategy, prioritizing Algorithmic Locality Optimization first, complemented by a RAM upgrade if necessary.**

1. **Why Algorithmic Locality is Essential:**
   - 3D medical scans are processed via slicing (e.g. $1024 \times 1024 \times 1024$ voxel arrays).
   - If the imaging algorithm traverses voxels along unaligned strides (e.g., column-major vs row-major), it touches a different 4 KB page on every voxel access, destroying cache and causing constant page faults even with 32 GB RAM when multiple patient datasets are loaded.
   - Restructuring the algorithm using **2D/3D cache-blocking (tiling)** keeps sub-volumes within L3 cache and RAM, reducing active working set size from 24 GB down to 2 GB per processing pass.
2. **When to Buy RAM:**
   - If the radiologist must run multiple 24 GB datasets concurrently, purchasing 32 GB of RAM ($<\$150$) is highly cost-effective to ensure the entire working set fits in physical memory, eliminating SSD write wear and unpredictable paging latency during surgical operations.

---

## 8. Alternative Concept & Complexity Analysis
**Alternative Concept:** Running on a machine with 32 GB RAM instead of relying on 16 GB demand paging.

### 1. EAT Comparison:
- **32 GB RAM (No Demand Paging Faults):**
  $$\text{EAT} = t_{\text{mem}} = \mathbf{100\text{ ns}}$$
- **16 GB RAM with $p = 10^{-4}$ Page Faults:**
  $$\text{EAT} = 100 + 0.0001 \times 7,999,900 = \mathbf{900\text{ ns}} \quad (\mathbf{9\times\text{ slower!}})$$

### 2. Financial & Cost-Benefit Analysis:
- The radiologist spends ~4 hours/day reviewing scans. A $9\times$ slowdown turns a 10-minute diagnostic reconstruction into a 90-minute wait, costing ~\$300/hour in clinical delay.
- An 8 GB - 16 GB RAM module costs approximately **\$50 - \$120** (one-off hardware expense).
- **Conclusion:** Upgrading RAM pays for itself within hours of physician productivity while preventing SSD endurance degradation from constant swap writes.
