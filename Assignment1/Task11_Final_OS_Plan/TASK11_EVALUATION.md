# Task 11: Recommend and Defend the Operating-System Plan

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Complete Smart Hospital Operating System Plan

| Tier | Hardware Platform | Operating System | Kernel Architecture | Key Services & Protection | I/O & Networking |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bedside Monitors (500 units)** | Dedicated Medical ARM SoC (512MB RAM) | **Hard RTOS (QNX Neutrino / seL4)** | Microkernel | Watchdog timer, fixed-priority preemptive scheduling, MPU sandbox | Interrupt-driven ADC, isolated UDP telemetry |
| **Nurses' Tablets (120 units)** | Enterprise Rugged Medical Tablets | **Hardened Android (AOSP Enterprise)** | Hybrid Monolithic | SELinux sandbox, biometric auth, wake-lock power governor | Wi-Fi 6 WPA3-Enterprise, BLE 5.2 |
| **Doctors' Workstations (80 units)** | 16-Core Intel Xeon, 32GB RAM, Quadro GPU | **Enterprise Linux (Ubuntu LTS / RHEL)** | Modular Monolithic | Multi-user PAM/Kerberos, X11/Wayland PACS viewer | Dual Gigabit Ethernet, NVMe SSD |
| **Central Database Server** | 2-Node Clustered Server (64 cores, 256GB RAM) | **Linux Cluster (RHEL with Pacemaker/Corosync)** | Modular Monolithic | High-availability active/passive failover, ACID durability, LUKS crypto | 25GbE LACP Bond, NVMe SAN |
| **MRI Imaging Server** | 4-Socket SMP Node (128 Cores, 512GB RAM, Tesla GPUs)| **HPC Linux (Rocky Linux with OpenMP/CUDA)** | Symmetric Multiprocessing | NUMA-aware CFS scheduler, CUDA runtime | PCIe Gen4 x16 DMA, 100GbE InfiniBand |
| **Partner Hospital Link**| Redundant High-Security Edge Gateways | **Hardened BSD / Linux Gateway (pfSense / VyOS)** | Monolithic Network Stack | Mutual TLS 1.3, WireGuard IPsec, Zero-Trust Access | Dedicated Encrypted Leased Fiber WAN |

---

## 2. Suitability for Scaling to a Group of Three Hospitals
When expanding from 1 hospital (500 monitors, 120 tablets, 80 workstations) to a network of 3 hospitals (1,500 monitors, 360 tablets, 240 workstations):
1. **Edge Scalability:** Bedside monitors and nurse tablets operate autonomously on localized hospital LAN subnets without overloading central WAN links.
2. **Database Sharding & Read Replicas:** Central database scales by deploying PostgreSQL streaming read replicas across all 3 hospital sites, while write transactions are routed to the clustered primary database via dedicated fiber links.
3. **PACS Imaging Federation:** MRI scans are cached locally at the originating hospital and fetched on-demand across partner links using compressed DICOM-web REST protocols.
