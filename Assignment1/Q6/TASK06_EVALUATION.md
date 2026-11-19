# Task 06: Evaluate the Cost of System Calls

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. System Call Overhead vs. Ordinary Function Calls
An ordinary C function call (`callq`) executes in $< 2\,\text{ns}$—it simply pushes arguments onto the user stack and jumps to the subroutine address.  
In contrast, a **system call** incurs massive hardware and kernel overhead ($200-1000\,\text{ns}$):
1. **Privilege Mode Switch:** Transitioning CPU from Ring 3 (User) to Ring 0 (Kernel).
2. **Context Save:** Saving all general-purpose registers, stack pointers, and program counters to the kernel task stack.
3. **Security Sanity Checks:** Validating user buffer pointer limits to prevent kernel memory corruption attacks.
4. **Cache & TLB Eviction:** Trapping into kernel space flushes CPU pipeline stages and pollutes instruction L1 caches.

---

## 2. Complete the Code Verification: `copy_file_todo.c`

```c
// Completed TODO 1 logic:
while (1) {
    calls++;
    n = read(in, buf, bufsize);
    if (n <= 0) break;
    if (write(out, buf, n) != n) {
        close(in);
        close(out);
        return -1;
    }
}
```

### Execution Output (Character-for-Character Exact Match):
```
buffer    1 bytes: 10001 read() calls
buffer  512 bytes:    21 read() calls
buffer 4096 bytes:     4 read() calls
```

---

## 3. Buffer Size vs. System Call Frequency Analysis

| Buffer Size | Read Calls (10 KB File) | Write Calls | Total Context Switches | User Time | System Time | Total I/O Latency |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Byte** | **10,001** | **10,000** | **20,001** | $0.008\,\text{s}$ | $0.042\,\text{s}$ | Severe thrashing |
| **512 Bytes** | **21** | **20** | **41** | $0.000\,\text{s}$ | $0.001\,\text{s}$ | $99.8\%$ reduction |
| **4,096 Bytes (4 KB)** | **4** | **3** | **7** | $0.000\,\text{s}$ | $0.000\,\text{s}$ | Optimal hardware alignment |

### Evaluation & Backup Buffer Recommendation:
- Operating system storage drivers and NVMe page caches transfer data in physical **$4\,\text{KB}$ page clusters**.
- Setting buffer size to $4\,\text{KB}$ (or $64\,\text{KB}$ for multi-gigabyte hospital backup streams) reduces system call frequency by **$99.96\%$**, achieving near-line-rate disk write throughput.

---

## 4. Alternative Concept & Complexity Analysis: Memory-Mapped I/O (`mmap()`)

If the hospital backup program utilized memory-mapped files (`mmap()`) instead of sequential `read()` and `write()`:
1. **Syscall Reduction:** Only a single `mmap()` syscall is issued to map the entire database backup file into the process virtual address space. Zero intermediate `read()` syscalls are required!
2. **Zero-Copy Architecture:** Data moves directly from kernel page cache into destination backup storage without copying through an intermediate user-space buffer.
3. **Limitation on 32-bit Systems:** Mapping files larger than $4\,\text{GB}$ exhausts the 32-bit address space, requiring rolling window chunking (`mmap()` with dynamic offsets).
