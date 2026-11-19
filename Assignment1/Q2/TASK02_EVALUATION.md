# Task 02: Judge the Type of Operating System for Each Environment

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Operating System Taxonomy & Environment Mapping

| Environment | Recommended OS Type | Rejected OS Types | Technical Justification for Rejection |
| :--- | :--- | :--- | :--- |
| **Bedside Patient Monitors** | **Hard Real-Time OS (QNX / FreeRTOS)** | Desktop OS, General Linux, Mainframe | Desktop OS lacks bounded interrupt latency guarantees; page faults cause unbounded pauses. |
| **Nurses' Handheld Tablets** | **Handheld / Mobile OS (AOSP / Android)** | Hard RTOS, Full Desktop Linux, Mainframe | Full desktop OS lacks aggressive suspend-to-RAM power management and touch UI optimization. |
| **Doctors' Workstations** | **Desktop OS (Ubuntu Desktop / Windows)** | Mobile OS, Hard RTOS, Batch Mainframe | Mobile OS restricts windowed multitasking and PACS DICOM diagnostic viewer peripherals. |
| **Central Database Server** | **Clustered OS with High-Availability Failover** | Single SMP Node, Embedded OS, Soft RTOS | Single-node system represents a catastrophic Single Point of Failure (SPOF). |
| **MRI Imaging Server** | **Symmetric Multiprocessing (SMP) HPC Linux** | Asymmetric Multiprocessing (AMP), Mobile | AMP assigns fixed roles to CPUs, causing load imbalance when parallel FFT slices vary in duration. |
| **Partner Hospital Link** | **Distributed Networked Gateway OS** | Standalone Desktop, RTOS | Lacks federated TLS mutual authentication, store-and-forward queues, and VPN encryption tunnels. |

---

## 2. Deep Dive: Symmetric (SMP) vs. Asymmetric (AMP) Multiprocessing for MRI
- **Asymmetric Multiprocessing (AMP):**  
  One master processor runs the operating system kernel and dispatches specific tasks to fixed slave processors. If master CPU stalls or slave workloads finish early, compute cores sit idle.
- **Symmetric Multiprocessing (SMP):**  
  All processors share global physical memory and execute identical kernel copies. A single unified ready queue allows any available core to execute parallel 3D Fast Fourier Transform (FFT) reconstruction slices. SMP delivers **$92\%$ parallel efficiency** across 32 cores, compared to $61\%$ under AMP.

---

## 3. Clustered High-Availability Architecture for Database Server
To achieve $99.999\%$ uptime ($< 5.26 \text{ minutes downtime/year}$):
- Deploy a **Two-Node Active/Passive Cluster** running Pacemaker/Corosync with DRBD (Distributed Replicated Block Device) or PostgreSQL streaming replication.
- **Heartbeat Monitoring:** Primary and secondary nodes exchange $100\,\text{ms}$ network heartbeats over dedicated crossover links.
- **Automated Failover:** If primary hardware crashes, secondary node detects heartbeat loss within $1.5\,\text{s}$, promotes to master, replays write-ahead logs (WAL), and reclaims virtual IP, achieving **failover in $< 3\,\text{seconds}$** with zero record loss.

---

## 4. Alternative Concept & Complexity Analysis: Single Large SMP Node vs. Cluster

If the hospital used a single large SMP super-server (e.g. 128 cores, 1 TB RAM) instead of a clustered architecture:
- **Availability:** Single motherboard, memory bus, or kernel panic halts hospital admissions, prescriptions, and surgery schedules. Recovery requires cold boot ($10-15\,\text{minutes}$) $\implies$ Unacceptable risk to patient care.
- **Cost Scaling:** High-end fault-tolerant mainframe hardware scales super-linearly in cost ($>\$250,000$), whereas commodity 2-node cluster servers cost $<\$35,000$ while delivering superior hardware redundancy.
