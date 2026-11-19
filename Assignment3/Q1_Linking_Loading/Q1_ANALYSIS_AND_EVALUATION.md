# Q1: Linking, Loading, and Address Binding — Evaluation & Analysis

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Linking, Loading, Address Binding (K5 - Evaluate, 6 Marks)  

---

## 1. Problem Context — Updating a Banking Application
A bank's branch software is built from many modules and libraries. When a security vulnerability is identified in the encryption library, every branch terminal must currently receive a massive new **200 MB static executable**. Across hundreds of branch locations with bandwidth-constrained WAN links, this creates unacceptable downtime, massive deployment overhead, and dangerous security delays.

### Core Objectives
1. Build and evaluate the application using **static linking** vs **dynamic (shared) linking**.
2. Measure and compare executable file sizes, startup times, and shared dependencies using `otool -L` / `ldd`.
3. Implement on-demand runtime loading using `dlopen()` and `dlsym()`.
4. Inspect process address spaces (`/proc/self/maps` and virtual memory regions).
5. Empirically verify hot-patching of the cryptographic library without recompilation.
6. Evaluate failure modes (missing shared libraries) and memory sharing across concurrent instances.

---

## 2. Theoretical Evaluation

### 2.1 Address Binding Phases
Address binding maps program instructions and data to physical memory addresses:
1. **Compile-Time Binding:**
   - If memory location is known *a priori*, absolute code is generated (e.g., embedded microcontrollers, DOS `.COM` files).
   - If starting address changes, full recompilation is mandatory.
2. **Load-Time Binding:**
   - Compiler produces relocatable code with symbolic references (offsets from base 0).
   - The OS loader binds relocatable addresses to physical memory addresses when the executable image is loaded into RAM. If the load address changes, reloading relocates addresses, but code cannot move during execution.
3. **Execution-Time (Dynamic Run-Time) Binding:**
   - Binding is delayed until execution time. The process can move between memory segments or pages during runtime (paging/swapping).
   - Requires hardware support (MMU with base and limit registers / page tables). This is the foundation of modern virtual memory OSes.

### 2.2 Roles of the Linker and Loader
```
[ Source Files .c ] ---> (Compiler gcc -c) ---> [ Object Files .o ]
                                                       |
[ Static Libraries .a ] ------------------------> [ LINKER (ld) ]
                                                       |
                                               [ Executable Binary ]
                                                       |
                                                (LOADER: execve)
                                                       |
                                      +----------------+---------------+
                                      |                                |
                            [ Static Address Space ]        [ Dynamic Linker ld.so ]
                                                            (Maps shared libraries .so/.dylib)
```
- **Linker (`ld`):** Resolves symbolic cross-references between compilation units, merges object code sections (`.text`, `.data`, `.rodata`, `.bss`), performs symbol relocation, and constructs an ELF or Mach-O executable.
- **Loader (`execve` / dynamic linker `ld.so`):** Allocates the process address space, maps segments into virtual memory, initializes data/BSS segments, sets up stack and heap pointers, resolves dynamic shared object references (via GOT/PLT), and transfers instruction control to `_start`.

### 2.3 Position-Independent Code (PIC)
Shared libraries must be loaded at arbitrary, non-conflicting virtual addresses in different processes.
- **PIC (`-fPIC`):** Generates machine code that uses relative addressing (PC-relative) rather than fixed absolute addresses.
- **Global Offset Table (GOT):** Stores absolute addresses of global variables in a private data page.
- **Procedure Linkage Table (PLT):** Trampolines function calls through lazy binding, resolving symbol targets upon their first execution.

---

## 3. Empirical Experimental Results

### 3.1 Binary Size & Deployment Footprint
| Artifact | Type | File Size | Deployment Payload |
|---|---|---|---|
| `bank_app_static` | Statically Linked Binary | **4.1 MB** (or 200 MB production) | Full 4.1 MB (recompile required) |
| `bank_app_dynamic` | Dynamically Linked Binary | **34 KB** | **0 KB** (Binary unchanged) |
| `libencrypt.dylib` (or `.so`) | Shared Dynamic Library | **4.0 MB** | **4.0 MB patch file only** |
| `bank_app_dlopen` | Runtime Loaded Binary | **33 KB** | **0 KB** (Binary unchanged) |

> **Key Takeaway:** For a 200 MB suite across 500 branches:
> - Static deployment: $500 \times 200\text{ MB} = \mathbf{100\text{ GB}}$ network transfer.
> - Dynamic patching: $500 \times 2\text{ MB} = \mathbf{1\text{ GB}}$ network transfer (**99% bandwidth savings**).

### 3.2 Dynamic Dependency Inspection
Output of `otool -L` / `ldd`:
```bash
$ otool -L bank_app_dynamic
bank_app_dynamic:
    @rpath/libencrypt.dylib (compatibility version 0.0.0, current version 0.0.0)
    /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1359.0.0)
```

### 3.3 Zero-Recompile Hot Patching Experiment
1. Initial run with `libencrypt_v1`:
   ```
   Active Security Module: v1.0.0-LEGACY (VULNERABLE: Weak XOR Cipher, CVE-2026-BANK-01)
   Security Patch Status : CRITICAL RISK (UNPATCHED)
   ```
2. Hot replace shared library:
   ```bash
   cp libencrypt_v2.dylib libencrypt.dylib
   ./bank_app_dynamic
   ```
3. Immediate output **without recompilation**:
   ```
   Active Security Module: v2.1.0-PATCHED (SECURE: ChaCha20-Poly1305 / AES-256-GCM Compliance)
   Security Patch Status : SECURE (PATCHED)
   ```
4. Verification against static executable:
   - `./bank_app_static` remained **vulnerable** (`v1.0.0-LEGACY`), proving that static linking locks vulnerable code permanently into binaries.

### 3.4 Missing Library Failure Comparison
| Approach | Missing Library Behavior | Impact on Bank Branch |
|---|---|---|
| **Dynamic Linking (Load-Time)** | OS Dynamic Linker halts execution immediately: `dyld: Library not loaded... Abort trap: 6` | Crash on boot; branch terminal completely inoperable. |
| **Dynamic Loading (`dlopen()`)** | `dlopen()` returns `NULL`, `dlerror()` provides diagnostics. Process continues in fallback mode. | Terminal detects error, logs event, alerts admin, and operates in offline/read-only mode. |

### 3.5 Multi-Instance Code Sharing
When multiple instances of `bank_app_dynamic` run simultaneously:
- The `__TEXT` (read-only executable code) pages of `libencrypt.dylib` (4 MB) are mapped **once** in physical memory.
- Both processes share the same physical frames via MMU virtual memory translation.
- Only private data pages (`.data` / `.bss`) invoke Copy-on-Write (COW).

---

## 4. Conclusion & Architectural Recommendation
**Which linking method should the bank use, and why?**

**Recommendation:** The bank should adopt **Dynamic (Shared) Linking with an automated plugin-based `dlopen()` architecture for security sub-modules**.

### Justification:
1. **Bandwidth & Patch Velocity:** When a zero-day vulnerability occurs, branches download only the 2 MB - 4 MB shared library instead of a 200 MB monolithic binary. Patches are effective immediately upon restart.
2. **Physical RAM Efficiency:** Multiple teller terminals on the same branch server share identical physical RAM pages for core business and encryption code.
3. **Resilience & Fault Isolation:** Critical security libraries loaded via `dlopen()` allow graceful degradation and security assertions rather than sudden application termination.

---

## 5. Alternative Concept & Complexity Analysis
**Alternative Concept:** Run-time on-demand dynamic loading with `dlopen()` / `dlsym()` exclusively when an encryption transaction is triggered, instead of linking dynamically at boot.

### 1. Evaluation:
- **Startup Time:** $O(1)$ fast initial application startup. The OS dynamic linker does not spend time parsing symbols, performing relocations, or binding library dependencies at launch.
- **Memory Footprint:** If a bank terminal is only performing inquiry tasks (balance checks, account lookup) that do not trigger cryptographic transfers, the 4 MB / 200 MB encryption library is **never mapped into virtual memory**, conserving RAM.
- **Error Handling:** Robust error interception. If the library file is corrupted or absent, `dlopen()` returns `NULL`, enabling the application to handle errors gracefully, switch to backup cryptography, or alert monitoring systems.

### 2. Complexity Analysis:
| Metric | Dynamic Linking at Startup (`ld.so`) | Dynamic Loading on Demand (`dlopen()`) |
|---|---|---|
| **Startup Time Complexity** | $O(N_{\text{sym}} + N_{\text{rel}})$ at process launch | $O(1)$ at launch; $O(M_{\text{sym}})$ deferred to first call |
| **Execution Overhead** | Near-zero (direct function pointer call via PLT/GOT) | $O(1)$ pointer dereference + initial symbol lookup cost |
| **Space Complexity (Idle RAM)** | $O(S_{\text{code}} + S_{\text{data}})$ mapped at boot | $0$ until function is explicitly needed |
| **Fault Resilience** | Low (Missing library kills process) | High (Programmable fallback & retry logic) |
