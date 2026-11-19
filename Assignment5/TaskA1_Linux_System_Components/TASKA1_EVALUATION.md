# Task A1: Evaluate the Linux System Components

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task A1.1: Linux Architecture & Kernel Subsystems
The Linux operating system comprises four primary layers:
1. **Hardware:** Physical CPU cores, DDR memory, NVMe storage, and network interface cards (NICs).
2. **Linux Kernel (Ring 0):** Monolithic modular core managing:
   - *Process Management:* Scheduler, IPC, signal delivery, process creation via `clone()`.
   - *Memory Management:* Paging, virtual memory areas, page cache, swap management.
   - *Virtual File System (VFS):* Standardized abstraction unifying ext4, XFS, NFS, and pseudofs.
   - *Device Drivers & Network Stack:* Netfilter packet filtering, socket queues, TCP/IP stack.
3. **System Libraries (Glibc):** Implements POSIX APIs, system call wrappers, and dynamic linkers (`ld-linux.so`).
4. **User-Space Utilities & Shell:** Interactive shells (bash), core utilities (coreutils), daemons (systemd).

---

## 2. Task A1.2: Process & Memory Management in Linux

### Completely Fair Scheduler (CFS):
- CFS allocates CPU time based on proportional fair-share scheduling using **Red-Black Trees** ($O(\log N)$ lookup time).
- Each runnable task tracks its execution time through **Virtual Runtime (`vruntime`)**:
  $$vruntime \mathrel{+}= \Delta \text{exec\_time} \times \frac{1024}{\text{weight}(\text{nice})}$$
- Tasks with lower nice values (higher priority) have higher weight, so their `vruntime` advances slower, granting them more frequent CPU scheduling turns.
- CFS automatically detects I/O-bound web processes (which sleep frequently waiting for database responses) and prioritizes them to ensure low interactive latency.

### The Page Cache, Swapping, and Kernel Observation:
- **Page Cache:** Linux automatically uses all unallocated physical RAM to cache disk blocks. Web portal static HTML, CSS, and database tables are cached in RAM, serving repeated requests in $< 100\,\text{ns}$ without touching physical SSD storage.
- **Swapping:** When physical memory pressure spikes, the kernel kswapd daemon reclaims anonymous memory pages and moves inactive pages to swap space.
- **/proc and /sys Pseudofilesystems:**
  - `/proc`: Runtime process information (`/proc/[pid]/status`, `/proc/meminfo`, `/proc/cpuinfo`).
  - `/sys`: Hardware device topology, cgroup resource limits, and kernel tunables (`/sys/fs/cgroup/`).

---

## 3. Task A1.3: Linux Directory Hierarchy, VFS, and Permission Model
- **Filesystem Hierarchy Standard (FHS):** Clean separation of binaries (`/bin`, `/usr/bin`), configurations (`/etc`), variable data (`/var/log`, `/var/www`), and mount points (`/mnt`, `/media`).
- **Virtual File System (VFS):** Provides an object-oriented abstraction using Inode objects, Dentry (directory entry) caches, and File objects, decoupling user applications from underlying physical storage formats.
- **Permissions & Security:** Standard discretionary access control (Owner, Group, Others) with read, write, execute bits (`rwxr-x---`). Enhanced with `setuid` binaries (e.g. `passwd`), `sudo` administrative privilege delegation, and POSIX capabilities (`CAP_NET_BIND_SERVICE`).

---

## 4. Alternative Concept & Complexity Analysis: Windows Server vs. Linux for Portal

If the University Result Portal ran on Windows Server (IIS + SQL Server) instead of Linux:
- **Base Memory & Disk Footprint:** Windows Server baseline installation requires $> 32\,\text{GB}$ disk space and $3-4\,\text{GB}$ idle RAM, compared to Linux ($1.5\,\text{GB}$ disk and $250\,\text{MB}$ idle RAM).
- **Automation Complexity:** Linux shell scripting and headless SSH automation enable fully automated zero-touch continuous deployment, whereas Windows historically relies on GUI wizards and PowerShell DSC with higher learning overhead.
- **Licensing Cost:** Commercial Windows Server and CAL (Client Access Licenses) for 150,000 students incur prohibitive licensing fees ($>\$100,000$), whereas Linux is open-source and free of licensing constraints.
