# Task 09: Evaluate the Memory Hierarchy and I/O Systems

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Storage Hierarchy in Healthcare Systems

| Hierarchy Level | Typical Access Time | Typical Capacity | Healthcare Data Placement Strategy |
| :--- | :---: | :---: | :--- |
| **CPU Registers** | $< 0.5\,\text{ns}$ | $1-2\,\text{KB}$ | Active loop variables, pointer offsets, encryption keys. |
| **L1 / L2 / L3 Cache** | $1 - 10\,\text{ns}$ | $64\,\text{KB} - 64\,\text{MB}$ | Active patient ECG rolling waveform buffers. |
| **Main Physical RAM** | $50 - 100\,\text{ns}$ | $16\,\text{GB} - 512\,\text{GB}$ | In-memory database buffer pool (PostgreSQL shared buffers). |
| **NVMe PCIe SSD** | $10 - 25\,\mu\text{s}$ | $2\,\text{TB} - 30\,\text{TB}$ | Active electronic health records (EHR) database tables. |
| **Secondary Hard Disk (HDD)**| $5 - 10\,\text{ms}$ | $50\,\text{TB} - 200\,\text{TB}$ | PACS long-term archived medical scans, historical logs. |
| **Cloud Object Storage (S3)**| $50 - 200\,\text{ms}$ | Unlimited (Petabytes)| Disaster recovery backups, multi-hospital federated archive. |

---

## 2. Programmed I/O vs Interrupt-Driven I/O vs DMA for MRI Scanners
- **Programmed I/O (PIO):** The CPU transfers every byte through I/O port registers (`in`/`out`). To transfer a single $500\,\text{MB}$ MRI scan, the CPU executes $125 \text{ Million}$ instructions, completely freezing doctor workstations.
- **Interrupt-Driven I/O:** The I/O controller interrupts the CPU on every word. For $500\,\text{MB}$, the CPU services $125 \text{ Million}$ interrupts. At $1\,\mu\text{s}$ per ISR, interrupt handling takes $125\,\text{seconds}$—vastly exceeding the scan duration!
- **Direct Memory Access (DMA):** The CPU writes the source memory buffer address and byte count to the DMA controller and resumes normal computation. The DMA engine streams all $500\,\text{MB}$ directly across the PCIe bus into system RAM via burst transfers, firing **exactly ONE single interrupt** upon total transfer completion.

---

## 3. Alternative Concept & Complexity Analysis: Interrupt-Driven I/O for 500 MB MRI Scans

If the MRI scanner used interrupt-driven I/O instead of PCIe bus-master DMA:
- **CPU Overhead:** Handling 125,000,000 interrupt service routines forces the processor into 100% kernel mode, causing complete workstation unresponsiveness and dropped network packets.
- **Transfer Throughput:** PCIe Gen4 x16 DMA streams data at **$28\,\text{GB/s}$**, transferring a $500\,\text{MB}$ MRI slice in **$17.8\,\text{milliseconds}$**, compared to over **$2 \text{ minutes}$** under interrupt-driven I/O.
