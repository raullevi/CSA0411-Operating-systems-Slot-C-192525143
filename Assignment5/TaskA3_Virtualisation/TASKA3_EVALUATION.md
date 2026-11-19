# Task A3: Evaluate Virtualisation

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task A3.1: Hypervisor Taxonomy & Hardware Virtualisation Support

| Feature | Type-1 Hypervisor (Bare-Metal) | Type-2 Hypervisor (Hosted) |
| :--- | :--- | :--- |
| **Architecture** | Runs directly on bare hardware; kernel is the hypervisor. | Runs as an application inside a host operating system. |
| **Examples** | KVM (Linux Kernel-based VM), VMware ESXi, Xen, Hyper-V. | VirtualBox, VMware Workstation, Parallels Desktop. |
| **Hardware Access** | Direct access to CPU VT-x/AMD-V and I/O MMU (VT-d). | Must arbitrate through host OS kernel drivers. |
| **Performance Overhead**| **Minimal ($1-3\%$ CPU overhead)**. | **Significant ($10-25\%$ CPU/memory overhead)**. |
| **Target Deployment** | Enterprise production servers, university data centers. | Developer local desktop testing, student labs. |

### Hardware Virtualisation Extensions:
- **Intel VT-x / AMD-V:** Adds hardware Root and Non-Root CPU operation modes. Guest operating systems execute privileged instructions directly in Ring 0 without binary translation traps (VM-Exit / VM-Entry).
- **Extended Page Tables (EPT / NPT):** Hardware handles two-dimensional page table walks (Guest Virtual Address $\to$ Guest Physical Address $\to$ Host Physical Address), drastically accelerating memory translation.

---

## 2. Task A3.2: Benefits and Costs of Virtual Machines for the University

### Key Operational Benefits:
1. **Server Consolidation:** Consolidates 10 separate department physical servers onto a single 64-core physical host, slashing electricity and cooling costs by $80\%$.
2. **Strong Fault & Security Isolation:** Hardware-enforced hypervisor boundaries ensure that a security breach in a student sandbox VM cannot access the adjacent examination database VM.
3. **Live Migration & High Availability:** KVM/QEMU supports migrating running VMs between physical hosts in $< 500\,\text{ms}$ with zero downtime during hardware maintenance.

### Costs & Overhead:
- **Duplicate Memory Consumption:** Every VM requires its own complete guest OS kernel, system libraries, and buffer caches ($2-4\,\text{GB}$ baseline RAM per VM).
- **Disk Footprint:** A full guest OS installation consumes $20-40\,\text{GB}$ of virtual disk space per VM.

---

## 3. Alternative Concept & Complexity Analysis: Type-2 (VirtualBox) vs. Type-1 (KVM)

If the university production portal were deployed inside VirtualBox running on a desktop host:
- **I/O Latency Collapse:** Every disk write and network packet traverses the guest OS $\to$ VirtualBox process $\to$ host OS kernel $\to$ physical NIC. Under 150,000 student result requests, host scheduler lock contention induces massive packet dropping.
- **KVM Direct Passthrough:** KVM transforms the Linux kernel into a Type-1 hypervisor using virtio drivers, achieving line-rate 10GbE network throughput and near-native NVMe performance.
