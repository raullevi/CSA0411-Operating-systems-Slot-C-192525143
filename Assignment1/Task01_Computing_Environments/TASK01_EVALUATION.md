# Task 01: Evaluate the Requirements of Each Computing Environment

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Smart Hospital Scenario & Environment Requirements Analysis
A 500-bed tertiary smart hospital replaces its legacy infrastructure with specialized computing tiers:
1. **Bedside Patient Monitors (500 units):** Continuous physiological monitoring (ECG, SpO2, blood pressure). **Hard real-time requirement: Must raise alarm within $\le 10\,\text{ms}$ of abnormal reading.**
2. **Nurses' Handheld Tablets (120 units):** Mobile electronic health records (EHR) entry and bedside barcode drug administration.
3. **Doctors' Desktop Workstations (80 units):** Clinical diagnosis, radiology visualization, and patient case reviews.
4. **Central Database Server:** Patient health records, laboratory orders, and medication logs. **Zero-downtime requirement (99.999% availability).**
5. **MRI Medical Imaging Server:** High-throughput 3D volumetric image reconstruction requiring multi-processor compute parallelism.
6. **Partner Hospital Federated Link:** Secure interconnect with two partner healthcare institutions sharing clinical trial and patient emergency records.

---

## 2. Requirement Matrix & Metric Prioritization

| Computing Environment | Primary Metric | Secondary Metric | Tolerance to Failure | Battery Life Requirement | Security Classification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bedside Monitor** | **Deterministic Latency ($\le 10\,\text{ms}$)** | Fault Isolation / 100% Uptime | **Zero (Life Critical)** | N/A (Mains + UPS backup) | High (Tamper resistance) |
| **Nurses' Tablet** | **Energy Efficiency ($> 12\,\text{h}$ shift)** | UI Usability & Fast Wifi Handover | Medium (Offline cache fallback) | **Critical ($> 12 \text{ hours}$)** | High (HIPAA / Biometric Auth) |
| **Doctors' Workstation** | **Interactive Throughput & Display Latency** | Software Multitasking Support | Low (Graceful app restart) | N/A (Mains Powered) | High (Role-Based Access) |
| **Central Database Server**| **High Availability (99.999%) & ACID Durability**| High Concurrent IOPS | **Zero (Cluster Failover $< 3\,\text{s}$)** | N/A (Dual Redundant PSUs) | **Maximum (Encrypted at Rest/Flight)** |
| **MRI Imaging Server** | **Computational Throughput (GFLOPS/TFLOPS)** | DMA Memory Bandwidth | Medium (Batch re-run permitted) | N/A (Data Center Rack) | Medium (Internal Vlan Protected) |
| **Partner Hospital Link**| **Cryptographic Security & TLS Latency** | Network Fault Tolerance | Low (Store-and-forward queue) | N/A (WAN Infrastructure) | **Maximum (Zero Trust / Mutual TLS)** |

---

## 3. Conflict Analysis & Trade-Off Resolutions
- **Conflict 1: Hard Real-Time Determinism vs. Multitasking Throughput (Bedside Monitor):**  
  General-purpose time-sharing schedulers (e.g. Linux CFS) maximize average throughput across many processes, but introduce unbounded scheduling delays during heavy load ($> 50\,\text{ms}$). This violates the $10\,\text{ms}$ life-safety alarm deadline.  
  *Resolution:* Dedicate a microkernel-based Hard Real-Time Operating System (RTOS) with fixed-priority preemptive scheduling for monitors.
- **Conflict 2: Battery Longevity vs. Background Processing (Handheld Tablets):**  
  Running continuous background sync services rapidly drains tablet battery within 3–4 hours, leaving nurses without charts during shifts.  
  *Resolution:* Aggressive OS power-management states (cgroups, DVFS frequency scaling, wake-lock restrictions, and push-based message queuing).

---

## 4. Alternative Concept & Complexity Analysis: General-Purpose OS Everywhere

If the entire hospital utilized a single general-purpose operating system (e.g. standard desktop/server Linux) across all 500 monitors, 120 tablets, workstations, and servers:
1. **Worst-Case Alarm Response Latency:**  
   Under kernel memory compaction, page faults, or disk logging, a standard Linux kernel can introduce unbounded dispatch latencies ($20\,\text{ms} \text{ to } 150\,\text{ms}$), causing fatal alarm suppression during cardiac arrest.
2. **Memory Footprint:**  
   Standard Linux requires $2\,\text{GB} \text{ to } 4\,\text{GB}$ RAM, whereas a microkernel RTOS requires only $8\,\text{MB} \text{ to } 32\,\text{MB}$, escalating hardware procurement costs by $10\times$ across 500 monitors.
3. **Administration Overhead:**  
   Managing monolithic OS patch cycles across mission-critical medical hardware requires frequent reboots and regression testing, increasing medical downtime risks.
