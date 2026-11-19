# Operating Systems Assignment 4 (CO4)
## Optimising File Storage and Disk Access

**Institution:** SIMATS Engineering, Saveetha Institute of Medical and Technical Sciences  
**Department:** Computer Science and Engineering  
**Course:** CSA0411 / CSA04 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Bloom's Taxonomy Level:** K5 – Evaluate  
**GitHub Repository:** [https://github.com/raullevi/CSA04-192525143-Assignment4.git](https://github.com/raullevi/CSA04-192525143-Assignment4.git)

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
CSA04-192525143-Assignment4/
├── Dockerfile                                 # Multi-platform container build
├── docker-compose.yml                         # Automated container test harness
├── run_all_tasks.sh                           # Master runner script
├── generate_terminal_screenshots.py           # Screenshot rendering utility
├── README.md                                  # Technical report & instructions
├── output_ss/                                 # Dedicated folder for terminal screenshots
│   ├── task02_output_screenshot.png
│   ├── task04_output_screenshot.png
│   └── task06_output_screenshot.png
├── Task01_FileSystem_Design_Review/ (Task01)  # Weakness analysis & tree design
├── Task02_Workload_to_FileAllocation/ (Task02)# Contiguous vs Indexed Inode (TODO)
├── Task03_Modern_File_Systems/ (Task03)       # ext4, XFS, ZFS, Btrfs, APFS
├── Task04_Disk_Scheduling_Algorithms/ (Task04)# FCFS, SSTF, SCAN, C-SCAN (TODO)
├── Task05_Distributed_and_Cloud_Storage/ (Task05) # NFS vs Ceph vs S3 & Device Mgmt
└── Task06_Design_Challenge_Video_Streaming/ (Task06) # Tiered NVMe/HDD start-up sim
```

---

## 3. Summary of Results for Tasks 1 – 6

| Task | Topic | Core Deliverable | Key Metric / Output | Evaluation Verdict |
| :---: | :--- | :--- | :--- | :--- |
| **Task 1** | **File System Review** | University 12k Namespace Architecture | B-Tree hierarchical lookup ($O(\log N)$) vs Flat ($O(N)$) | Rejected flat directory; implemented tree with POSIX ACLs. |
| **Task 2** | **File Allocation** | Complete `file_alloc_todo.c` (TODO 1) | **Output:** `E (10 blocks) contiguous: start 19`, `indexed: index block 6` | Proved external fragmentation in contiguous; selected ext4/XFS extents. |
| **Task 3** | **Modern File Systems** | File System Comparison Matrix | Analyzed CoW vs Journaling (`data=ordered`) | Defended XFS for databases, APFS for laptops, ZFS for backups. |
| **Task 4** | **Disk Scheduling** | Complete `disk_sched_todo.c` (TODO 1) | **Output:** FCFS (640), SSTF (236), SCAN (236), C-SCAN (183 + 199 jump) | Proved SSTF starves far requests; defended C-SCAN & `mq-deadline`. |
| **Task 5** | **Cloud & Distributed** | Storage Evaluation & Device Mgmt | 3-way replication in Ceph vs single NFS SPOF | Evaluated strong vs eventual consistency under CAP theorem. |
| **Task 6** | **Design Challenge** | Video Streaming 200k Students Sim | **Design B (Tiered NVMe): $1.73\,\text{ms}$ seek ($4.9\times$ speedup vs HDD $8.5\,\text{ms}$)** | Defended 2-second HLS chunking on NVMe cache + HDD cold archive. |

---

## 4. Execution Commands

```bash
chmod +x run_all_tasks.sh
./run_all_tasks.sh
```
