# Operating Systems Assignment 2 (CO2)
## Process Management, CPU Scheduling, POSIX Threads, IPC, Synchronisation & Deadlock Handling

**Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences  
**Department:** Computer Science and Engineering  
**Course:** CSA0411 / CSA04 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Bloom's Taxonomy Level:** K5 – Evaluate  
**GitHub Repository:** [https://github.com/raullevi/CSA04-192525143-Assignment2.git](https://github.com/raullevi/CSA04-192525143-Assignment2.git)

---

## 1. Environment & Compilation Details
- **Operating System:** Ubuntu 22.04 LTS (x86_64 / arm64) via Docker / Darwin POSIX Kernel
- **Compiler:** GCC 13+ / Apple LLVM Clang 15+
- **C Standard:** C11 (`-std=c11`)
- **Compilation Flags:** `-std=c11 -Wall -Wextra -pthread -O2`
- **Containerization:** Docker (`Dockerfile`) and Docker Compose (`docker-compose.yml`)

---

## 2. Directory Structure & Deliverables

```
CSA04-192525143-Assignment2/
├── Dockerfile                                 # Multi-platform container build
├── docker-compose.yml                         # Automated container test harness
├── run_all_tasks.sh                           # Master runner script
├── generate_terminal_screenshots.py           # Screenshot rendering utility
├── README.md                                  # Comprehensive technical report
├── output_ss/                                 # Dedicated folder for terminal screenshots
│   ├── task01_output_screenshot.png
│   ├── task02_output_screenshot.png
│   ├── task03_output_screenshot.png
│   ├── task04_output_screenshot.png
│   ├── task05_output_screenshot.png
│   └── task06_output_screenshot.png
├── Task01_Processes_and_States/ (Task01 / Q1) # Online Exam Server Simulation
│   ├── Makefile, process_tree_sim.c, run_q1_experiments.sh
│   ├── experiment_q1_results.log, Q1_ANALYSIS_AND_EVALUATION.md
├── Task02_CPU_Scheduling/ (Task02 / Q2)       # Cloud Video-Encoding Suite
│   ├── Makefile, cpu_scheduling_todo.c, cpu_scheduler_suite.c
│   ├── experiment_q2_results.log, Q2_ANALYSIS_AND_EVALUATION.md
├── Task03_POSIX_Threads/ (Task03 / Q3)        # Traffic Camera Plate Reader
│   ├── Makefile, camera_threads.c, run_q3_experiments.sh
│   ├── experiment_q3_results.log, Q3_ANALYSIS_AND_EVALUATION.md
├── Task04_IPC_Pipelines/ (Task04 / Q4)        # Weather Station Data Pipeline
│   ├── Makefile, pipe_ipc_todo.c, ipc_comparison_bench.c
│   ├── experiment_q4_results.log, Q4_ANALYSIS_AND_EVALUATION.md
├── Task05_Synchronization_Primitives/ (Task05 / Q5) # Railway Ticket Booking
│   ├── Makefile, sync_todo.c, railway_booking_sim.c
│   ├── experiment_q5_results.log, Q5_ANALYSIS_AND_EVALUATION.md
└── Task06_Deadlock_Bankers/ (Task06 / Q6)     # Lab Equipment Scheduler
    ├── Makefile, bankers_todo.c, bankers_scale_bench.c
    ├── experiment_q6_results.log, Q6_ANALYSIS_AND_EVALUATION.md
```

---

## 3. Summary of Results for Tasks Q1 – Q6

| Task | Topic | Core Deliverable | Key Metric / Output | Evaluation Verdict |
| :---: | :--- | :--- | :--- | :--- |
| **Q1** | **Processes & States** | Process Tree Simulation & Fork Benchmarking | Fork + Teardown: $\approx 880\,\mu\text{s}$, $15\,\text{MB}$ PCB overhead for 2,000 sessions | Rejected process-per-student; adopted fixed worker pool reactor. |
| **Q2** | **CPU Scheduling** | Round Robin TODO & Scheduling Suite | **Gantt:** `P1(0-3) P2(3-6) P3(6-9) P4(9-12) P1(12-15) P2(15-16) P3(16-19) P4(19-21) P1(21-23) P3(23-26)`<br>Avg TAT = $20.00$, Avg WT = $13.50$ | Recommended 3-level MLFQ with aging for video encoding. |
| **Q3** | **POSIX Threads** | 64-Camera Multithreading & Race Condition | Thread pool 8 workers: $4.77\times$ speedup; Unprotected counter lost $103+$ updates | Defended thread pools matching physical cores; atomic counters. |
| **Q4** | **IPC Pipelines** | Pipe IPC TODO & 100MB Benchmark | **Analyser:** `6 readings, average 35.5, max 41`<br>Pipe: $5.1\,\text{GB/s}$ vs SHM: $4.3\,\text{GB/s}$ | Identified pipe EOF semantics when parent closes write fd; SHM for bulk. |
| **Q5** | **Synchronisation** | Bounded Buffer & Railway Booking Sim | **Output:** `items consumed: 20, sum = 210`<br>100/100 runs verified; Per-coach lock gives $2.3\times$ speedup | Rejected global locking; recommended per-coach fine-grained locking. |
| **Q6** | **Deadlock & Banker's** | Banker's Algorithm & Quadratic Scaling | **Output:** Initial safe `P1 P3 P4 P0 P2`, P1 granted, P4 waits, P0 denied (unsafe) | Proved $O(m \cdot n^2)$ scaling; recommended detection + checkpointing. |

---

## 4. Execution Commands

### Quick Automated Run (All Tasks):
```bash
chmod +x run_all_tasks.sh
./run_all_tasks.sh
```

### Running in Docker:
```bash
docker-compose up --build
```

### Compiling and Running Individual Tasks:
```bash
# Task 01:
cd Task01_Processes_and_States && make && ./process_tree_sim

# Task 02:
cd Task02_CPU_Scheduling && make && ./cpu_scheduling_todo && ./cpu_scheduler_suite

# Task 03:
cd Task03_POSIX_Threads && make && ./camera_threads

# Task 04:
cd Task04_IPC_Pipelines && make && ./pipe_ipc_todo && ./ipc_comparison_bench

# Task 05:
cd Task05_Synchronization_Primitives && make && ./sync_todo && ./railway_booking_sim

# Task 06:
cd Task06_Deadlock_Bankers && make && ./bankers_todo && ./bankers_scale_bench
```
