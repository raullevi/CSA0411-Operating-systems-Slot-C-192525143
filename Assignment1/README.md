# Operating Systems Assignment 1 (CO1)
## Evaluate and Justify the Operating-System Design of a Smart Hospital

**Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences  
**Department:** Computer Science and Engineering  
**Course:** CSA0411 / CSA04 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Bloom's Taxonomy Level:** K5 – Evaluate  
**GitHub Repository:** [https://github.com/raullevi/CSA04-192525143-Assignment1.git](https://github.com/raullevi/CSA04-192525143-Assignment1.git)

---

## 1. Environment & Compilation Details
- **Operating System:** Ubuntu 22.04 LTS via Docker / Darwin POSIX Kernel
- **Compiler:** GCC 13+ / Apple LLVM Clang 15+
- **C Standard:** C11 (`-std=c11`)
- **Compilation Flags:** `-std=c11 -Wall -Wextra -pthread -O2`
- **Execution Script:** `./run_all_tasks.sh`

---

## 2. Directory Structure & Deliverables

```
CSA04-192525143-Assignment1/
├── Dockerfile                                 # Multi-platform container build
├── docker-compose.yml                         # Automated container test harness
├── run_all_tasks.sh                           # Master runner script
├── generate_terminal_screenshots.py           # Screenshot rendering utility
├── README.md                                  # Technical report & instructions
├── output_ss/                                 # Dedicated folder for terminal screenshots
│   ├── task06_output_screenshot.png
│   ├── task07_output_screenshot.png
│   └── task10_output_screenshot.png
├── Task01_Computing_Environments/ (Task01/Q1) # Hospital Requirements & Conflicts
├── Task02_OS_Types/ (Task02/Q2)               # OS Types (RTOS, Clustered, SMP vs AMP)
├── Task03_OS_Structures/ (Task03/Q3)          # Microkernel vs Monolithic vs Modular
├── Task04_OS_Services/ (Task04/Q4)            # Service Pruning & Attack Surface
├── Task05_System_Calls_Walkthrough/ (Task05/Q5)# Syscall Anatomy (read step-by-step)
├── Task06_Cost_of_System_Calls/ (Task06/Q6)   # copy_file TODO (buffer 1, 512, 4096)
├── Task07_Process_Control/ (Task07/Q7)        # shell_todo (fork, execlp, waitpid)
├── Task08_CPU_States_Protection/ (Task08/Q8)  # Dual mode, Timer interrupts, Polling
├── Task09_Memory_Hierarchy_IO/ (Task09/Q9)    # Storage hierarchy, DMA for MRI
├── Task10_Measure_and_Compare/ (Task10/Q10)   # 1000 processes vs 1000 threads benchmark
├── Task11_Final_OS_Plan/ (Task11/Q11)         # Complete Hospital Architecture
└── Task12_Day4_Design_Challenge/ (Task12/Q12) # Edge Wearables & Cloud Migration
```

---

## 3. Summary of Results for Tasks 1 – 12

| Task | Topic | Core Deliverable | Output / Verdict |
| :---: | :--- | :--- | :--- |
| **Task 1** | **Requirements** | Ranked Requirements & Conflict Analysis | Prioritized $\le 10\,\text{ms}$ deterministic alarm for patient safety over throughput. |
| **Task 2** | **OS Types** | OS Classification & Failover Architecture | Hard RTOS (Monitors), Android (Tablets), Clustered Active/Passive (Database). |
| **Task 3** | **Structures** | Microkernel vs Monolithic Evaluation | Microkernel for monitors (driver fault isolation); Modular monolithic for database. |
| **Task 4** | **Services** | OS Service Pruning Matrix | Pruned shells, paging, and display managers from monitors to guarantee deadline. |
| **Task 5** | **System Calls** | Step-by-step `read()` Syscall Walkthrough | Documented mode switch (Ring 3 $\to$ 0), register ABI, trap, and return. |
| **Task 6** | **Cost of Syscalls** | Complete `copy_file_todo.c` | **Output:** `buffer 1: 10001 calls`, `buffer 512: 21 calls`, `buffer 4096: 4 calls`. |
| **Task 7** | **Process Control**| Complete `shell_todo.c` | **Output:** `shell: running job 1`, `42`, `status 0`, `job 2 exit status 3`. |
| **Task 8** | **CPU States** | Dual-Mode & Timer Interrupt Analysis | Timer preempts runaway loops; privileged `CLI` stops rogue interrupt disabling. |
| **Task 9** | **Memory & I/O** | Storage Hierarchy & DMA for MRI Scanners | Bus-master DMA streams 500MB MRI in $17.8\,\text{ms}$ (vs 125M interrupts in PIO). |
| **Task 10**| **Benchmark** | 1,000 Processes vs 1,000 Threads | **Threads: $16.99\,\mu\text{s}$ ($49.1\times$ faster than processes: $834.52\,\mu\text{s}$).** |
| **Task 11**| **Final Plan** | Full Hospital Plan & 3-Hospital Scaling | Edge autonomy + central replicated cluster handles network of 3 hospitals. |
| **Task 12**| **Design Challenge**| Remote Home Wearables & Cloud Records | Hybrid Edge-Cloud: Zephyr RTOS on home wearables + Kubernetes EKS in cloud. |

---

## 4. Execution Commands

```bash
chmod +x run_all_tasks.sh
./run_all_tasks.sh
```
