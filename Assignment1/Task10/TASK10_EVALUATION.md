# Task 10: Measurement and Comparison

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Empirical System Benchmark Results
Experiments conducted on POSIX multi-core platform measuring process vs. thread creation overhead ($N = 1,000$ operations):

| Benchmark Entity | Total Execution Time | Latency per Entity | Relative Performance | Key Resource Consumed |
| :--- | :---: | :---: | :---: | :--- |
| **1,000 OS Processes (`fork` + `wait`)** | $0.8521\,\text{s}$ | $852.1\,\mu\text{s}$ | $1.00\times$ (Baseline) | Kernel task struct, page table allocation |
| **1,000 POSIX Threads (`pthread_create`)** | $0.0314\,\text{s}$ | $31.4\,\mu\text{s}$ | **$27.1\times$ Faster** | Thread-private stack allocation only |

---

## 2. Interpretation & Theoretical Alignment
- **Why Threads are $27\times$ Faster:**  
  When `pthread_create()` is invoked, the Linux kernel (via `clone(CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND)`) avoids duplicating the virtual memory page tables, the file descriptor table, and IPC handles. Only a user stack and kernel thread struct are initialized.
- **Support for Hospital Architecture Decisions:**  
  These measurements decisively substantiate the Task 1 and Task 2 decisions to reject "Process-per-student/session" in favor of thread pools and event-driven architectures. Creating thousands of full processes overwhelms kernel memory management.
