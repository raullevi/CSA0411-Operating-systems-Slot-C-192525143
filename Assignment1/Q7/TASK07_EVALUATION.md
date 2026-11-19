# Task 07: Evaluate Process Control System Calls

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Process Control Fundamentals in Operating Systems
In UNIX systems, process creation and lifecycle execution are modularized across distinct primitive system calls:
- `fork()`: Creates a new child process with an exact duplicate address space (using Copy-On-Write page tables).
- `execve()` / `execlp()`: Replaces the current process virtual memory, text, data, and stack segments with a fresh executable image from disk, retaining open file descriptors unless flagged with `FD_CLOEXEC`.
- `waitpid()`: Blocks the calling parent until the child process changes state (terminates or halts), returning termination exit status.
- `exit()` / `_exit()`: Terminates the calling process. `exit()` flushes stdio library buffers and invokes `atexit` handlers; `_exit()` terminates immediately in kernel space.

---

## 2. Complete the Code Verification: `shell_todo.c`

```c
// Completed TODO 1 logic:
pid_t pid1 = fork();
if (pid1 < 0) {
    perror("fork failed");
    exit(1);
} else if (pid1 == 0) {
    execlp("expr", "expr", "6", "*", "7", (char *)NULL);
    exit(127);
} else {
    int status1;
    waitpid(pid1, &status1, 0);
    printf("job 1 exit status %d\n", WEXITSTATUS(status1));
}
```

### Execution Output (Character-for-Character Exact Match):
```
shell: running job 1
42
job 1 exit status 0
shell: running job 2
job 2 exit status 3
```

---

## 3. Deep Dive: Buffer Flushing Before `fork()` & The Duplicate Output Phenomenon

### Why `stdout` Must Be Flushed Before `fork()`:
- The standard C library (`stdio.h`) buffers output in user space.
  - Line-buffered when connected to a terminal (`\n` flushes automatically).
  - Block-buffered ($4\,\text{KB}$) when redirected to a file or pipe (`./shell_todo > out.txt`).
- When `printf("shell: running job 2\n")` is executed into a block-buffered stream, the characters remain sitting in the parent's user-space heap buffer without being written to the kernel.
- When `fork()` is called, the child inherits an identical copy of the parent's dirty `stdout` buffer.
- If the child terminates via `exit(3)` instead of `_exit(3)`, the C library cleanup routines in BOTH parent and child flush the identical dirty buffer to the file descriptor, causing `"shell: running job 2"` to appear **TWICE** in the output log!
- Preemptively calling `fflush(stdout)` forces the buffer to commit to the kernel before the address space is cloned.

---

## 4. Zombies, Orphans, and the `init` / `systemd` Reaper
- **Zombie Process:** A child process that has called `exit()` but whose parent has not yet invoked `wait()` or `waitpid()`. Its entry in the kernel process table (`task_struct`) persists to preserve exit codes.
- **Orphan Process:** A child whose parent terminated without reaping it. The operating system kernel automatically re-parents the orphan to PID 1 (`init` / `systemd`), which continuously executes `wait()` to prevent zombie accumulation.

---

## 5. Alternative Concept & Complexity Analysis: `posix_spawn()` vs. `fork() + exec()`

- **`fork() + exec()` Overhead:** For a large database server process holding $64\,\text{GB}$ of memory mappings, calling `fork()` requires copying millions of page table entries ($64 \times 8\,\text{KB} = 512\,\text{KB}$ of page structures), even though the subsequent `exec()` will immediately discard them.
- **`posix_spawn()` Architecture:** Implements a direct kernel-level spawn without page table duplication, accelerating command execution by **$8-15\times$** on memory-dense database hosts.
