# CSA0411 Operating Systems — Assignment 3 (CO3)

**Course Outcome (CO3):** Evaluate memory-management mechanisms such as linking, paging, and segmentation to determine their effectiveness for different system requirements — linking and loading, paging, segmentation, virtual memory, demand paging, page-replacement techniques, and disk management.

---

## Student & Environment Information
- **Student Name:** Rakul K
- **Register Number:** `192525143`
- **Course Code & Slot:** CSA0411 (Operating Systems) — Slot C
- **Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences
- **Bloom's Taxonomy Level:** **K5 - Evaluate** (Every task evaluated at K5 level)
- **Total Marks:** 50 Marks
- **GitHub Repository Link:** [https://github.com/raullevi/CSA0411-Operating-systems-Slot-C-192525143.git](https://github.com/raullevi/CSA0411-Operating-systems-Slot-C-192525143.git)
- **C Compiler & Version:** `gcc` (Apple Clang version 21.0.0 / GCC 13+ compatible)
- **Compilation Standard & Flags:** `gcc -std=c11 -Wall -Wextra -pthread -O2`
- **Platform / Operating System:** macOS Darwin 27.0.0 (ARM64) / Linux Ubuntu 22.04+ (POSIX-compliant)

---

## Assignment Architecture & Principle
Every question is designed, implemented, analysed, and evaluated under the K5 cognitive rubric:
$$\text{Design} \longrightarrow \text{Implementation} \longrightarrow \text{Analysis} \longrightarrow \text{Evaluation}$$

### Progressive Commit History
In strict adherence to the assignment guidelines, this repository features progressive commits corresponding to each milestone:
1. `feat(Q1): implement linking, loading, and address binding experiments and evaluation`
2. `feat(Q2): implement paging address translation, complete the code, and evaluation`
3. `feat(Q3): implement segmentation translation, SIGSEGV handler, and fragmentation analysis`
4. `feat(Q4): implement virtual memory benchmarks, EAT calculations, COW test, and fault curve`
5. `feat(Q5): implement page replacement algorithms, complete the code, Belady anomaly, and Clock analysis`
6. `feat(Q6): implement disk I/O benchmarks, RAID reliability model, swap analysis, and evaluations`
7. `feat(Q7): implement edge memory management plan from first principles, mlock benchmark, and defense`
8. `docs: complete master report, README documentation, and automated test suite`

---

## Repository Structure

```
CSA0411-Operating-systems-Slot-C-192525143/
├── README.md                                # Master documentation & instructions
├── run_all_tasks.sh                         # Unified master execution script
├── .gitignore                               # Clean repository tracking
├── Q1_Linking_Loading/                      # [6 Marks] Linking, Loading & Address Binding
│   ├── Makefile                             # Build rules for static, dynamic, dlopen
│   ├── libencrypt.h                         # Cryptographic module interface header
│   ├── libencrypt_v1.c                      # Vulnerable encryption implementation (v1.0)
│   ├── libencrypt_v2.c                      # Patched encryption implementation (v2.1)
│   ├── bank_app.c                           # Banking application client (static & dynamic)
│   ├── bank_app_dlopen.c                    # Dynamic runtime loading via dlopen() & dlsym()
│   ├── run_q1_experiments.sh                # Automated benchmark and hot-patch test script
│   ├── experiment_q1_results.log            # Execution log and memory inspection
│   └── Q1_ANALYSIS_AND_EVALUATION.md        # Comprehensive technical report & analysis
├── Q2_Paging/                               # [8 Marks] Paging & Complete the Code
│   ├── Makefile                             # Build rules for paging programs
│   ├── paging_todo.c                        # Complete the Code (PAGE_SIZE 1024 & 2048)
│   ├── paging_sim.c                         # 100-process fragmentation and EMAT simulator
│   ├── run_q2_experiments.sh                # Automated testing script
│   ├── experiment_q2_results.log            # Program output & verification logs
│   └── Q2_ANALYSIS_AND_EVALUATION.md        # Mathematical calculations, EMAT, diagrams
├── Q3_Segmentation/                         # [6 Marks] Segmentation & Protection
│   ├── Makefile                             # Build rules
│   ├── segmentation_sim.c                   # 8-address translation, SIGSEGV trap, frag sim
│   ├── run_q3_experiments.sh                # Test runner and vmmap segment inspector
│   ├── experiment_q3_results.log            # Execution output log
│   └── Q3_ANALYSIS_AND_EVALUATION.md        # Segmented paging diagrams, comparison table
├── Q4_Virtual_Memory/                       # [8 Marks] Virtual Memory & Demand Paging
│   ├── Makefile                             # Build rules
│   ├── vm_experiments.c                     # Locality benchmark, COW fork test, fault curve
│   ├── plot_curve.py                        # Python vector SVG curve generator
│   ├── page_fault_curve.csv                 # Raw simulation datapoints
│   ├── page_fault_curve.svg                 # Vector visualization: Faults vs Frames
│   ├── run_q4_experiments.sh                # Execution script
│   ├── experiment_q4_results.log            # Execution log
│   └── Q4_ANALYSIS_AND_EVALUATION.md        # EAT math, thrashing, working-set analysis
├── Q5_Page_Replacement/                    # [8 Marks] Page Replacement & Complete the Code
│   ├── Makefile                             # Build rules
│   ├── page_replacement_todo.c             # Complete the Code (LRU, FIFO, Optimal, Belady)
│   ├── replacement_engine.c                 # Full suite: Clock algorithm, 100k benchmark
│   ├── plot_replacement.py                  # Python vector SVG curve generator
│   ├── page_replacement_workload.csv        # Workload metrics for frames 3 to 10
│   ├── page_replacement_workload.svg        # Vector graph: Algorithm fault comparison
│   ├── run_q5_experiments.sh                # Test runner
│   ├── experiment_q5_results.log            # Output log
│   └── Q5_ANALYSIS_AND_EVALUATION.md        # Stack property proof, hardware analysis
├── Q6_Disk_Management/                      # [4 Marks] Disk Management & Hospital Server
│   ├── Makefile                             # Build rules
│   ├── disk_benchmark.c                     # Sequential & random I/O benchmark
│   ├── raid_calculator.c                    # RAID capacity & reliability loss model
│   ├── run_q6_experiments.sh                # Benchmark runner & partition inspector
│   ├── experiment_q6_results.log            # Output log
│   └── Q6_ANALYSIS_AND_EVALUATION.md        # Boot blocks, swap design, RAID 10 selection
└── Q7_Memory_Management_Plan/               # [10 Marks] Edge Device Design from First Principles
    ├── Makefile                             # Build rules
    ├── rt_memory_lock_benchmark.c           # mlock() determinism vs unlocked jitter benchmark
    ├── edge_device_memory_sim.c             # 2 GB edge simulation, 4th-task mitigation
    ├── run_q7_experiments.sh                # Simulation and verification runner
    ├── experiment_q7_results.log            # Verification output log
    └── Q7_ANALYSIS_AND_EVALUATION.md        # 4-stage first principles derivation & defense
```

---

## Quick Start & Complete Execution

To execute every program and experiment across all 7 tasks simultaneously:
```bash
chmod +x run_all_tasks.sh
./run_all_tasks.sh
```

---

## Task Summaries & Key Results

### Q1: Linking, Loading and Address Binding (6 Marks)
- **Problem Context:** Bank branches receiving 200 MB monolithic executable updates when only the encryption library was patched.
- **Key Findings:**
  - `bank_app_static` embedded the entire 4 MB module (4.1 MB binary). Recompilation and full redeployment required for every patch.
  - `bank_app_dynamic` was only **34 KB**. When `libencrypt_v2.dylib` was copied into place, the application instantly upgraded to the secure cipher **without recompilation**!
  - `bank_app_dlopen` (runtime loading) allowed graceful error handling when the library was absent, preventing sudden crash traps.
- **Conclusion:** Bank must adopt dynamic shared linking with automated versioned hot-patching.

### Q2: Paging & Complete the Code (8 Marks)
- **Problem Context:** Multi-user college server suffering from severe external fragmentation under contiguous allocation.
- **Completed Code (`paging_todo.c`):**
  - Matched exact expected prompt output for `PAGE_SIZE = 1024`:
    - `0 -> physical 5120`, `1500 -> physical 2524`, `3100 -> physical 7196`, `6200 -> physical 3128`, `9000 -> invalid address`, `2049 -> page fault`.
  - Recalculated by hand for `PAGE_SIZE = 2048`: Address 9000 mapped to physical 808, address 2049 mapped to physical 4097 without page faults.
- **Calculations & Simulation:**
  - 32-bit flat page table: **4 MB per process**.
  - 48-bit flat page table: **512 GB per process** (proves hierarchical paging is mandatory).
  - 100-process simulation showed 4 KB paging limits internal fragmentation to 0.72%, whereas 2 MB huge pages waste 86.05% of memory for small student scripts.

### Q3: Segmentation & Protection (6 Marks)
- **Problem Context:** Segregating read-only shared compiler code, stack expansion, and variable data structures.
- **Key Findings:**
  - Verified 8 address translations: offset boundary checks caught buffer overflows and off-by-one errors with `SIGSEGV` traps.
  - Caught hardware MMU fault using `sigaction` (`SA_SIGINFO`), documenting kernel exception escalation from Ring 3 to Ring 0.
  - 20-segment simulation demonstrated **81.09% external fragmentation** (550 KB free across 11 holes, but a 150 KB request was rejected due to lack of contiguous space).
- **Conclusion:** Modern operating systems rely on paging because it eliminates external fragmentation entirely.

### Q4: Virtual Memory and Demand Paging (8 Marks)
- **Problem Context:** Radiologist running 24 GB medical imaging software on a 16 GB laptop.
- **Calculations:**
  - For $t_{\text{mem}} = 100\text{ ns}$ and $t_{\text{fault}} = 8\text{ ms}$:
    - $p = 1/1,000 \implies \text{EAT} = 8,099.9\text{ ns}$ (**$81\times$ slowdown!**).
    - $p = 1/100,000 \implies \text{EAT} = 180.0\text{ ns}$ (**$1.8\times$ slowdown**).
    - $p = 1/1,000,000 \implies \text{EAT} = 108.0\text{ ns}$ (**$8\%$ slowdown**).
  - Maximum acceptable fault rate for $\le 10\%$ slowdown: $p \le 1.25 \times 10^{-6}$ (**1 fault in 800,000 accesses**).
- **Experiments:** Verified Copy-on-Write (COW) with `fork()`, observing zero duplicate memory until write operations occurred. Plotted the working-set knee curve (`page_fault_curve.svg`).
- **Conclusion:** Priority is algorithmic cache-blocking/tiling to minimize active working sets, complemented by a RAM upgrade for multi-patient workflows.

### Q5: Page-Replacement Techniques (8 Marks)
- **Problem Context:** Web server caching frequently requested pages.
- **Completed Code (`page_replacement_todo.c`):**
  - 3 frames: FIFO 15, LRU 12, Optimal 9.
  - 4 frames: FIFO 10, LRU 8, Optimal 8.
  - Bélády's Anomaly demonstrated on string `1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5`: FIFO faults increased from 9 to 10 with 4 frames! LRU decreased from 10 to 8.
- **100,000 References Benchmark:**
  - Clock (second-chance) algorithm achieved within **1.8% of exact LRU** (53.45% vs 51.57% faults) while operating with $1/64\text{th}$ of the hardware overhead (a single reference bit vs 64-bit timestamps).
- **Engineering Decision:** Recommended the Clock algorithm for web servers.

### Q6: Disk Management (4 Marks)
- **Problem Context:** Hospital records server requiring 24/7 boot reliability, disk failure survival, and peak swap capacity.
- **RAID Calculations (6 Disks $\times$ 4 TB = 24 TB Raw):**
  - RAID 0: 24 TB, 0 fault tolerance.
  - RAID 1: 12 TB (mirrored pairs).
  - RAID 5: 20 TB, survives 1 disk, $4\times$ write penalty.
  - RAID 6: 16 TB, survives 2 disks, $6\times$ write penalty.
  - RAID 10: 12 TB, survives up to 3 disks, $2\times$ write penalty.
- **Data Loss Model:** RAID 5 has a **$30\times$ higher probability of catastrophic data loss** during an active rebuild than RAID 10 due to rebuild stress and Unrecoverable Read Errors (URE).
- **Conclusion:** Recommended RAID 10 on NVMe SSDs with a dedicated mirrored swap partition.

### Q7: Memory Management Plan from First Principles (10 Marks)
- **Problem Context:** Smart factory edge device with **2 GB RAM and NO swap disk**. Runs Real-Time Control, 1.5 GB Machine Learning, Telemetry Logging, and future tasks.
- **Stage 1 (Problem Interpretation):** Identified RT control requires 0 page faults and $<50\ \mu\text{s}$ latency; ML needs 1.5 GB; Total active budget = 1,856 MB / 2,048 MB (192 MB safety buffer).
- **Stage 2 (Mechanism Comparison):** Selected Paged Virtual Memory with `mlockall()` and stack pre-faulting for RT control, paired with `cgroups v2` memory capping for ML.
- **Stage 3 (Implementation & Verification):** `rt_memory_lock_benchmark.c` verified $0$ page faults and deterministic sub-microsecond latency. Simulation confirmed $0$ deadline misses across 10,000 cycles.
- **Stage 4 (Defense & 4th Task Analysis):**
  - Adding a 500 MB task causes a 308 MB deficit, triggering the Linux OOM killer!
  - Engineered two mitigation solutions: (1) `zram` compressed in-memory swap (+307 MB RAM gain), (2) ML Model Quantization (FP32 $\to$ INT8), shrinking model from 1.5 GB to 384 MB and liberating 1,152 MB of RAM.
- **Alternative Concept:** Evaluated RTOS vs Linux with locked memory.

---

## Verification & Compilation Commands

### 1. Compile and Run Question 1
```bash
cd Q1_Linking_Loading
make clean && make
./bank_app_dynamic
./bank_app_dlopen ./libencrypt.dylib
./run_q1_experiments.sh
```

### 2. Compile and Run Question 2
```bash
cd Q2_Paging
make clean && make
./paging_todo
./paging_sim
./run_q2_experiments.sh
```

### 3. Compile and Run Question 3
```bash
cd Q3_Segmentation
make clean && make
./segmentation_sim
./run_q3_experiments.sh
```

### 4. Compile and Run Question 4
```bash
cd Q4_Virtual_Memory
make clean && make
./vm_experiments
python3 plot_curve.py
./run_q4_experiments.sh
```

### 5. Compile and Run Question 5
```bash
cd Q5_Page_Replacement
make clean && make
./page_replacement_todo
./replacement_engine
python3 plot_replacement.py
./run_q5_experiments.sh
```

### 6. Compile and Run Question 6
```bash
cd Q6_Disk_Management
make clean && make
./raid_calculator
./disk_benchmark
./run_q6_experiments.sh
```

### 7. Compile and Run Question 7
```bash
cd Q7_Memory_Management_Plan
make clean && make
./rt_memory_lock_benchmark
./edge_device_memory_sim
./run_q7_experiments.sh
```

---
*Submitted for CSA0411 Operating Systems Assessment — SIMATS Engineering.*
