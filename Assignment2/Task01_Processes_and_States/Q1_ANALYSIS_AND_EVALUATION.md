# Task 01: Processes and Process States - Online Examination Server

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Problem Context: Online Examination Server Bottleneck
In an online examination management system, the server spawns an independent OS process for every logged-in student session, along with auxiliary helper processes for periodic auto-saving of written answers and real-time proctoring video stream ingestion. During exam commencement, when **2,000 students** log in simultaneously, the server experiences severe degradation: response latency spikes exponentially, CPU utilization hits 100%, and numerous sessions appear completely frozen or "hung".

---

## 2. Process-State Transition Diagram
An operating system process undergoes five standard lifecycle states:

```
           +-------------------------------------------------------+
           |                                                       |
           v                                                       |
     +-----------+       Admit        +-----------+   Scheduler   +-----------+
     |    NEW    | -----------------> |   READY   | ------------> |  RUNNING  |
     +-----------+                    +-----------+   Dispatch    +-----------+
                                            ^                           |
                                            |   Timer / Preemption      |
                                            +---------------------------+
                                            |                           |
                                            | I/O or Event              | I/O or Event
                                            | Completion                | Wait
                                            |                           v
                                      +---------------------------------------+
                                      |                WAITING                |
                                      |              (BLOCKED)                |
                                      +---------------------------------------+
                                                                        |
                                                                        | Exit / Terminate
                                                                        v
                                                                  +-----------+
                                                                  |TERMINATED |
                                                                  |  (ZOMBIE) |
                                                                  +-----------+
```

### State Definitions:
1. **New:** The process is being created via `fork()` or `clone()`. The kernel allocates a new Task Structure (`task_struct`), allocates a unique Process Identifier (PID), and initializes the Process Control Block (PCB).
2. **Ready:** The process resides in main memory and is queued on the OS Ready Queue (e.g., Linux Completely Fair Scheduler `cfs_rq`). It is waiting for the CPU scheduler to allocate a time slice.
3. **Running:** The CPU is actively executing the process's instructions in user space or kernel space via system calls.
4. **Waiting (Blocked):** The process cannot execute because it is waiting for an external event or I/O operation (e.g., incoming HTTP packet from a student, answer database write completion, or video frame read). It yields the CPU and sleeps on a wait queue.
5. **Terminated (Zombie):** The process has finished execution via `exit()` or received a fatal signal. Its address space and file descriptors are deallocated, but its entry in the process table remains until the parent calls `wait()` or `waitpid()` to collect its exit status.

---

## 3. Process Control Block (PCB) Architecture
The kernel represents each process through a **Process Control Block** (on Linux, `struct task_struct` in `<linux/sched.h>`):

| PCB Component | Purpose & Contents in Exam Server Context |
| :--- | :--- |
| **Process Identifier (PID & PPID)** | Unique integer identifying student session process and parent server daemon PID. |
| **Process State** | Flag indicating `TASK_RUNNING`, `TASK_INTERRUPTIBLE` (I/O sleep), `TASK_UNINTERRUPTIBLE`, `EXIT_ZOMBIE`. |
| **Program Counter (PC)** | Register holding the memory address of the next instruction to execute. |
| **CPU Registers** | State of general-purpose registers (RAX, RBX, RCX, RDX, RSP, RBP, RSI, RDI, flags) saved during context switch. |
| **CPU Scheduling Information** | Process priority, nice value (`-20` to `+19`), dynamic virtual runtime (`vruntime`), scheduling policy (`SCHED_NORMAL`). |
| **Memory Management Info** | Pointers to page directory tables (`pgd`), segment registers, base and limit registers, virtual memory areas (`vm_area_struct`). |
| **Accounting Information** | CPU time used (`utime`, `stime`), wall-clock execution limits, context switch counters (`nvcsw`, `nivcsw`). |
| **I/O Status Information** | Open file descriptor table (`fd_array` pointing to socket handles, database pipes, log file streams). |

---

## 4. Evaluation: Where Does the Time Go with 2,000 Active Processes?

When 2,000 distinct processes run concurrently on a server with 8 or 16 physical CPU cores, system performance collapses due to three primary bottlenecks:

### A. Context Switch Overhead & CPU Thrashing
- With 2,000 processes competing for 16 CPU cores, each core must juggle 125 processes.
- A process context switch requires saving CPU registers to the PCB, reloading the memory management registers (CR3 register reload), and invalidating the **Translation Lookaside Buffer (TLB)**.
- Each context switch costs approximately $5 \text{ to } 15\,\mu\text{s}$. If processes yield or are preempted 1,000 times per second, the system spends:
  $$\text{Overhead} = 2,000 \times 1,000 \times 10\,\mu\text{s} = 20,000,000\,\mu\text{s/sec} = 20 \text{ CPU-seconds/sec}$$
  On a 16-core machine, **more than 100% of several CPU cores is completely wasted on context switching alone**, leaving insufficient compute time for actual student workload processing.
- Cache thrashing: Since each student process has a distinct address space, L1/L2/L3 CPU caches are continuously flushed and polluted, resulting in severe cache misses.

### B. Memory Footprint and Virtual Memory Thrashing
- Even with Copy-On-Write (COW) semantics from `fork()`, each student process requires:
  - Kernel task struct and kernel stack: $8\,\text{KB} \text{ to } 16\,\text{KB}$.
  - User-space stack, heap, and runtime page tables: typically $4\,\text{MB} \text{ to } 16\,\text{MB}$ per active process.
- For 2,000 processes, total RAM requirement is:
  $$\text{RAM} \approx 2,000 \times 8\,\text{MB} = 16\,\text{GB}$$
- When video proctoring processes (buffering webcam frames) and auto-save processes are added, memory consumption escalates to $30+\,\text{GB}$, forcing the OS into swap space on secondary disk. Swap I/O latencies ($10\,\text{ms}$) are $100,000\times$ slower than RAM ($100\,\text{ns}$), resulting in catastrophic system lockups.

### C. I/O Wait Latency and Lock Contention
- In an online exam, students type intermittently (human think time). Processes spend >95% of their time in `TASK_INTERRUPTIBLE` waiting for socket events or database disk writes.
- 2,000 processes simultaneously attempting to append auto-saved answers create massive lock contention on disk journal buffers, database connection pools, and network socket queues.

> **Evaluation Judgment:** Creating **one process per student is fundamentally unsound and architecturally broken** for high-concurrency web workloads.

---

## 5. Design Decision: Process vs Thread vs Fixed Worker Pool

| Architecture | Memory per Session | Context Switch Cost | Fault Isolation | Concurrency Scalability | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **One Process per Student** | High ($4-16\,\text{MB}$) | High ($5-15\,\mu\text{s}$ + TLB flush) | Complete (Isolated address space) | Terrible ($< 500$ processes before collapse) | **Rejected** |
| **One Thread per Student** | Moderate ($0.5-2\,\text{MB}$ stack) | Moderate ($1-2\,\mu\text{s}$, shared TLB) | None (Single thread crash kills server) | Mediocre ($1,000-2,000$ max threads) | **Suboptimal** |
| **Fixed Pool of Worker Threads / Event Loop** | Minimal ($< 100\,\text{KB}$ per active connection) | Negligible ($O(1)$ event dispatch, 0 thread switches for idle sessions) | Robust (Workers isolated from network connections) | Outstanding ($10,000-100,000+$ concurrent sessions) | **RECOMMENDED & DEFENDED** |

### Defense of Recommended Decision:
The optimal architecture is an **Asynchronous Non-blocking Event-Driven Reactor** (e.g., Linux `epoll` or macOS `kqueue`) coupled with a **Fixed Pool of Worker Threads** (sized to $N_{\text{cores}}$):
1. **Zero thread-per-session penalty:** 2,000 student sockets are monitored by a single `epoll` listener thread using negligible memory.
2. **Predictable resource utilization:** Worker threads handle computational tasks (cryptographic exam token verification, proctoring ML inference) without exceeding physical core capacity, completely eliminating context-switch thrashing.
3. **Graceful degradation:** Incoming bursts are queued in memory buffers rather than triggering kernel process allocation failures.

---

## 6. Alternative Concept & Complexity Analysis: Thread-per-Session vs Process-per-Session

If each student session were implemented as a thread inside a single server process:
- **Memory Consumption:** Instead of allocating complete page tables, memory maps, and standard library segments ($4\,\text{MB}$ to $16\,\text{MB}$), each POSIX thread requires only its private stack allocation (configurable between $64\,\text{KB}$ and $2\,\text{MB}$). Total memory for 2,000 sessions decreases from $16\,\text{GB}$ to $200\,\text{MB}$—an **$80\times$ reduction**.
- **Context Switch Latency:** POSIX threads within the same process share the same page directory (CR3 register). Therefore, thread switching involves only saving/restoring CPU general registers and the stack pointer (RSP), preserving TLB entries. Thread context switch cost is approximately $1\,\mu\text{s}$, compared to $10\,\mu\text{s}$ for a full process switch—a **$10\times$ speedup**.
- **Vulnerability to Cascading Failure:** The fatal flaw of a pure thread-per-session architecture is memory space sharing: a single null pointer dereference, buffer overflow, or unhandled exception in one student's video packet parser triggers a `SIGSEGV`, instantly terminating the entire server process and disconnecting all 2,000 students simultaneously.

### Complexity Comparison:
- **Process Creation Time Complexity:** $O(N)$ with large constant factor ($k \approx 400\,\mu\text{s}$ due to Page Table duplication and memory mapping).
- **Thread Creation Time Complexity:** $O(N)$ with small constant factor ($k \approx 20\,\mu\text{s}$ due to stack allocation without page table clone).
- **Event-Driven Reactor Scaling:** Space complexity is $O(N)$ connection descriptors; Scheduling time complexity is $O(1)$ per ready event via `epoll_wait()`.
