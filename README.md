# SIMATS Engineering - Operating Systems Course Portfolio (CO1 – CO5)

**Student Name:** Rakul K  
**Register Number:** 192525143  
**Course Code:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences  
**Bloom's Level Assessed:** K5 – Evaluate  
**Primary Repository:** [https://github.com/raullevi/CSA0411-Operating-systems-Slot-C-192525143.git](https://github.com/raullevi/CSA0411-Operating-systems-Slot-C-192525143.git)

---

## Portfolio Architecture & Directory Structure
This repository contains the complete laboratory submissions for all five Course Outcomes (CO1 to CO5) of the Operating Systems course. Each assignment is structured in its own self-contained directory with source code, build scripts, execution logs, and high-resolution terminal output screenshots:

```
├── Assignment1/     # CO1: Operating System Architectures (Smart Hospital Workload)
│   ├── Task01 .. Task12
│   ├── output_ss/   # Dark-mode terminal output screenshots
│   └── *.docx       # Official SIMATS submission reports
├── Assignment2/     # CO2: Process Management, Concurrency & Deadlocks
│   ├── Q1 .. Q6
│   ├── output_ss/   # Dark-mode terminal output screenshots
│   └── *.docx       # Official SIMATS submission reports
├── Assignment3/     # CO3: Memory Management & Paging
│   ├── Q1 .. Q7
│   ├── output_ss/   # Dark-mode terminal output screenshots
│   └── *.docx       # Official SIMATS submission reports
├── Assignment4/     # CO4: Optimising File Storage & Disk Access
│   ├── Task01 .. Task06
│   ├── output_ss/   # Dark-mode terminal output screenshots
│   └── *.docx       # Official SIMATS submission reports
├── Assignment5/     # CO5: Linux, Containers & Virtualisation for Efficient Operations
│   ├── TaskA1 .. TaskB4
│   ├── output_ss/   # Dark-mode terminal output screenshots
│   └── *.docx       # Official SIMATS submission reports
└── Reports/         # Comprehensive Word (.docx) submission reports for all COs
```

---

## Course Outcomes & Assignment Summary

### [Assignment 1: CO1 - Operating System Architectures](file:///Assignment1/)
- **Domain:** Smart Hospital Patient Monitoring & ICU Automation.
- **Key Tasks:** System calls (`copy_file_todo.c`), interactive shell (`shell_todo.c`), 1000 processes vs 1000 threads benchmark (`measure_bench.c`), kernel vs user memory isolation.
- **Output Screenshots:** `Assignment1/output_ss/`

### [Assignment 2: CO2 - Process Management & Deadlocks](file:///Assignment2/)
- **Domain:** City Surveillance, Traffic Light Sensing & Railway Seat Allocation.
- **Key Tasks:** Process trees (`process_tree_sim.c`), CPU scheduling FCFS/SJF/RR/MLFQ (`cpu_scheduling_todo.c`), 64-camera thread safety (`camera_threads.c`), IPC Pipes vs Shared Memory (`pipe_ipc_todo.c`), Bounded-buffer synchronization (`sync_todo.c`), Banker's safety algorithm and unsafe state proof (`bankers_todo.c`).
- **Output Screenshots:** `Assignment2/output_ss/`

### [Assignment 3: CO3 - Memory Management & Paging](file:///Assignment3/)
- **Domain:** In-Memory Database & Multiprogramming Systems.
- **Key Tasks:** Static vs dynamic linking & ELF loading (`Q1`), Two-level paging address translation (`Q2`), Segmentation (`Q3`), Demand paging & page faults (`Q4`), Page replacement algorithms FIFO/LRU/Optimal (`Q5`), Disk track management (`Q6`), Enterprise memory plan (`Q7`).
- **Output Screenshots:** `Assignment3/output_ss/`

### [Assignment 4: CO4 - Optimising File Storage & Disk Access](file:///Assignment4/)
- **Domain:** Video Streaming Platform & Academic Media Archive.
- **Key Tasks:** Flat vs hierarchical directory trees (`Task 1`), Contiguous first-fit vs indexed inode allocation (`file_alloc_todo.c`), Journaling file systems matrix ext4/XFS/ZFS (`Task 3`), Disk scheduling FCFS/SSTF/SCAN/C-SCAN (`disk_sched_todo.c`), Distributed storage NFS vs Ceph vs S3 (`Task 5`), Tiered NVMe/HDD storage simulation for 200,000 students (`video_storage_sim.c`).
- **Output Screenshots:** `Assignment4/output_ss/`

### [Assignment 5: CO5 - Linux, Containers & Virtualisation](file:///Assignment5/)
- **Domain:** University Result Portal & Cloud Operations.
- **Key Tasks:** Linux server administration & AWK log analytics (`access_log_summary.sh`), Automated disk alert monitor (`disk_alert.sh`), Multi-stage secure containerisation (`Dockerfile`, `docker-compose.yml`), Bare Metal vs VM vs Container benchmark, Kubernetes Deployment manifest & self-healing verification (`deployment.yaml`), Multi-service resource quotas & 150,000 student capacity sizing model (`TaskB4`).
- **Output Screenshots:** `Assignment5/output_ss/`

---

## Official Submission Reports (.docx)
All generated submission documents comply with SIMATS Engineering standards, Bloom's Level K5 evaluation rubrics, code listings, execution logs, and dark-mode terminal output figures:
1. `Reports/Rakul_K_192525143_CSA0411_Assignment1_Answers.docx`
2. `Reports/Rakul_K_192525143_CSA0411_Assignment2_Answers.docx`
3. `Reports/Rakul_K_192525143_CSA0411_Assignment3_Answers.docx`
4. `Reports/Rakul_K_192525143_CSA0411_Assignment4_Answers.docx`
5. `Reports/Rakul_K_192525143_CSA0411_Assignment5_Answers.docx`

---

## Execution Instructions
To execute any assignment, navigate to its respective directory and run the test harness:
```bash
# Assignment 1
cd Assignment1 && ./run_all_tasks.sh

# Assignment 2
cd Assignment2 && ./run_all_tasks.sh

# Assignment 3
cd Assignment3 && ./run_all_tasks.sh

# Assignment 4
cd Assignment4 && ./run_all_tasks.sh

# Assignment 5
cd Assignment5 && ./run_all_tasks.sh
```
