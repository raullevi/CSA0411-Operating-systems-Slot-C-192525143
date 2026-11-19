# Task 05: Examine System Calls

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. System Call Architecture & Categories
System calls serve as the fundamental programmatic interface between a user-mode application and privileged OS kernel services:
1. **Process Control:** `fork()`, `execve()`, `waitpid()`, `exit()`, `getpid()`.
2. **File Management:** `open()`, `read()`, `write()`, `close()`, `unlink()`.
3. **Device Management:** `ioctl()`, `read()`, `write()`.
4. **Information Maintenance:** `gettimeofday()`, `alarm()`, `sysinfo()`.
5. **Communication:** `pipe()`, `shmget()`, `socket()`, `connect()`, `send()`, `recv()`.
6. **Protection:** `chmod()`, `chown()`, `umask()`.

---

## 2. Step-by-Step Anatomy of a `read()` System Call
When an electronic medical record software calls `read(fd, buffer, count)`:
1. **User Space C Library Wrapper:** User program executes `read()`, which invokes the GNU C library (`glibc`) wrapper.
2. **Parameter Marshaling:** Glibc loads arguments into designated hardware registers (on x86-64: `RDI` = file descriptor, `RSI` = buffer pointer, `RDX` = byte count). The syscall number for `sys_read` (`0`) is loaded into `RAX`.
3. **Trap / Mode Switch:** The processor executes the `syscall` assembly instruction (or software interrupt `int 0x80`). The CPU hardware switches privilege level from User Mode (Ring 3) to Kernel Mode (Ring 0), saves RIP and RFLAGS to the kernel stack, and jumps to the System Call Entry Point (`system_call_entry`).
4. **Kernel Verification & Work:** The kernel indexes the system call dispatch table (`sys_call_table[RAX]`), verifies that the user pointer in `RSI` is valid and writeable, checks open file descriptor permissions, consults the VFS inode and page cache, and initiates block storage transfer.
5. **Return & Privilege Restoration:** Once data is copied into the user buffer, the kernel sets the return value (bytes read) in `RAX`, executes `sysretq`, restoring Ring 3 user mode. The application resumes execution.

---

## 3. Alternative Concept & Complexity Analysis: C Library Buffering vs. Direct System Calls

- **Direct Syscalls (`read()` / `write()`):** For a file of size $N$ bytes with buffer $b$, the program incurs:
  $$\text{Syscall Count} = \lceil \frac{N}{b} \rceil$$
  If $b = 1\,\text{byte}$, a $10\,\text{KB}$ file triggers $10,001$ kernel mode transitions.
- **Library Buffering (`fread()` / `fwrite()`):** Glibc allocates an internal $4\,\text{KB}$ page buffer in user space. Calling `fgetc()` $10,000$ times incurs only $\lceil 10,000 / 4096 \rceil = 3$ actual `read()` system calls, reducing kernel context-switch overhead by **$99.97\%$**.
