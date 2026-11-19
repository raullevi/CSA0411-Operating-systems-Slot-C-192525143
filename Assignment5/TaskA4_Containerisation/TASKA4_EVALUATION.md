# Task A4: Evaluate Containerisation

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task A4.1: How Containers Work (Namespaces, Cgroups, and Image Layers)

Unlike virtual machines that emulate hardware, containers are **isolated user-space processes running directly on the host Linux kernel**:
1. **Linux Namespaces (Isolation Boundaries):**
   - `PID Namespace`: Process IDs are re-mapped; container application sees itself as PID 1.
   - `NET Namespace`: Dedicated virtual network interface (`veth`), routing table, and private ports.
   - `MNT Namespace`: Isolated filesystem mount hierarchy.
   - `UTS Namespace`: Private hostname and domain.
   - `IPC Namespace`: Isolated shared memory segments and semaphores.
   - `USER Namespace`: Maps container root (`uid=0`) to an unprivileged user on the host.
2. **Control Groups (cgroups v2 - Resource Governance):**
   - Enforces hard and soft resource limits on CPU quota (`cpu.max`), memory ceiling (`memory.max`), block I/O bandwidth (`io.weight`), and task count (`pids.max`).
3. **OverlayFS (Union Filesystem & Image Layering):**
   - Images are composed of read-only immutable layers (Base OS $\to$ Dependencies $\to$ App Code).
   - When a container starts, a thin read-write scratch layer is mounted on top. Multiple container instances share the identical read-only image layers in memory via Copy-on-Write, eliminating storage duplication.

---

## 2. Task A4.2: Containers vs. Virtual Machines Comparison

| Metric / Dimension | Virtual Machines (KVM / VMware) | Containers (Docker / Podman) |
| :--- | :--- | :--- |
| **Start-Up Time** | $30 - 90\,\text{seconds}$ (Full OS boot cycle) | **$< 1\,\text{second}$ (Instant process fork)** |
| **Memory Footprint** | $1 - 4\,\text{GB}$ baseline per VM | **$20 - 50\,\text{MB}$ per container** |
| **Image / Disk Size** | $10 - 50\,\text{GB}$ per virtual disk | **$50 - 200\,\text{MB}$ (using python:3.12-slim)** |
| **CPU / I/O Efficiency** | Minor hypervisor translation tax ($2-5\%$) | **$100\%$ Native Bare-Metal Speed** |
| **Isolation Strength** | **Hardware-Level (Hypervisor Ring -1)** | **OS-Level (Shared Linux Kernel)** |
| **Role in Portal Architecture** | Best for Stateful Database (PostgreSQL) | Best for Stateless Web Replicas (Flask/Gunicorn) |

---

## 3. Alternative Concept & Complexity Analysis: VM-per-Instance vs. Container-per-Instance

If the university scaled the Result Portal by spawning 50 Virtual Machines instead of 50 Docker Containers:
- **RAM Waste:** 50 VMs require $50 \times 2\,\text{GB} = \mathbf{100\,\text{GB RAM}}$ just to boot guest kernels. 50 containers consume only $50 \times 60\,\text{MB} = \mathbf{3\,\text{GB RAM}}$, allowing 30x higher instance density on the same hardware.
- **Autoscaling Responsiveness on Result Day:** When 150,000 students log in, containers spin up in $500\,\text{ms}$, instantly absorbing traffic surges. VMs require 2 minutes to boot, causing connection timeouts and server crash loops.
