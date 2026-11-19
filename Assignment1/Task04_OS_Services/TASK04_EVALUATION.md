# Task 04: Evaluate the Services an Operating System Must Provide

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Operating System Service Matrix Across Hospital Environments

| OS Service | Bedside Monitor | Nurses' Tablet | Doctors' Workstation | Central Database | MRI Imaging Server |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **User Interface (GUI)** | Minimal (Dedicated Canvas) | **Full Touch UI** | **Full Windowed Desktop** | **None (Headless CLI)** | Web/Console Admin |
| **Program Execution & Sched** | Fixed-Priority Real-Time | Fair-Share Preemptive | CFS Time-Sharing | High-Throughput CFS | High-Performance NUMA |
| **File System Management** | Minimal Flash Log (Raw SPI) | SQLite / Flash Encrypted | Full Ext4/APFS | **Enterprise XFS / ZFS** | High-Speed Scratch NVMe |
| **I/O Device Operations** | Low-Latency ADC / Serial | Touchscreen, Camera, Barcode | Multi-monitor, GPU, Mouse | NVMe SAN / RAID Array | High-Speed PCIe DMA |
| **Communication / Network** | Isolated Telemetry UDP/CAN | Wi-Fi 6 + Bluetooth BLE | Gigabit Ethernet | Dual 25GbE LACP Bond | 100GbE InfiniBand |
| **Protection & Security** | Memory MPU Sandboxing | App Sandboxing / SELinux | Multi-user RBAC | Row-Level Security / TLS | VLAN Segmented |
| **Error Detection & Logging** | Hardware Watchdog Timer | Centralized Crashlytics | Systemd Journald | Auditd / Remote Syslog | Hardware ECC Machine Check |

---

## 2. Service Pruning for Bedside Monitors
To guarantee real-time determinism ($\le 10\,\text{ms}$) and prevent memory exhaustion:
- **Pruned Services:** General-purpose interactive shell (bash/sh), virtual memory demand paging/swap, desktop display managers (X11/Wayland), dynamic package managers, complex file systems with indexing, and legacy device drivers.
- **Retained Services:** Hardware Watchdog timer service, preemptive real-time scheduler, isolated ADC/SPI sensor driver, raw framebuffer renderer, and lightweight UDP telemetry streaming.

---

## 3. Alternative Concept & Complexity Analysis: Full Desktop OS on Handheld Tablets

If the nurses' tablets executed a full desktop OS with all background daemons enabled (printing spoolers, SSH daemons, search indexers):
- **Storage & Memory Footprint:** Desktop OS consumes $20\,\text{GB}$ flash storage and $2.5\,\text{GB}$ baseline RAM, leaving insufficient memory for high-resolution medical imaging charts.
- **Battery Life Collapse:** Continuous background indexing and unoptimized power states drain battery within $2.5 \text{ hours}$ (compared to $14 \text{ hours}$ on a streamlined mobile OS), interrupting patient drug administration rounds.
