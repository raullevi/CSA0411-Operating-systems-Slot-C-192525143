# Q6: Disk Management — Evaluation & Analysis

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Disk Management, Formatting, Boot Process, Swap Space, RAID Architecture (K5 - Evaluate, 4 Marks)  

---

## 1. Problem Context — Storage for a Hospital Records Server
A regional hospital operates a mission-critical electronic health records (EHR) server. 
- **Core Requirements:**
  1. The server must **start reliably without boot failure** (24/7 emergency room availability).
  2. The storage system must **survive the physical failure of a disk drive** without data corruption or offline downtime (zero patient record loss).
  3. The system must allocate **sufficient swap space** to prevent application crashes during peak concurrent diagnostic image loading.

---

## 2. Disk Formatting, Boot Blocks, and Bad Block Management

```
Disk Formatting Hierarchy:
+---------------------------------------------------------------------------------+
| 1. Low-Level Formatting (Physical sectors, headers, trailers, ECC bytes)       |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| 2. Partitioning (Partition table: MBR or GPT; divides disk into slices)         |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| 3. Logical Formatting (Filesystem creation: ext4, XFS, NTFS; Superblocks, Inodes)|
+---------------------------------------------------------------------------------+
```

### 2.1 Disk Formatting Stages
1. **Low-Level (Physical) Formatting:**
   - Performed at the factory. Fills disk surfaces with physical tracks and sectors.
   - Writes sector headers, sector trailers, preamble data, and **Error-Correcting Code (ECC)** checksums (e.g. Reed-Solomon or LDPC).
2. **Partitioning:**
   - Divides the raw physical storage into logical block ranges.
   - Managed via **Master Boot Record (MBR)** (legacy 32-bit, max 2 TB) or **GUID Partition Table (GPT)** (modern standard, 64-bit LBA, redundant headers, supports $>2\text{ TB}$ disks).
3. **Logical (High-Level) Formatting:**
   - The OS constructs file system data structures on a partition (e.g., ext4, XFS, APFS).
   - Initializes superblocks, inode tables, free-space allocation bitmaps, and the root directory.

### 2.2 Boot Block and The Bootstrapping Process
1. **POST (Power-On Self-Test):** Motherboard firmware initializes CPU, DRAM, and storage controllers.
2. **UEFI / BIOS Initialization:** Firmware locates the boot device configured in NVRAM.
3. **EFI System Partition (ESP) / MBR Boot Code:**
   - Firmware loads the initial stage boot code from the EFI System Partition (FAT32) or Master Boot Record (first 512 bytes, LBA 0).
4. **Bootloader Execution (e.g., GRUB2 / systemd-boot):**
   - The bootloader reads configuration files, loads the kernel image (`vmlinuz`) and initial RAM disk (`initrd` / `initramfs`) into RAM.
5. **Kernel & Systemd Hand-Off:**
   - Kernel takes control of hardware, probes disk controllers, mounts the root filesystem (`/`), and launches PID 1 (`systemd`), which starts EHR hospital database daemons.

### 2.3 Handling Bad Blocks
- **Sector Sparing (Forwarding):**
  - Storage controllers reserve hidden spare tracks at the inner/outer cylinder boundaries.
  - When the drive controller detects a failing sector during an ECC read failure, it marks the sector defective in the internal defect list and transparently redirects subsequent I/O to a spare sector.
- **Sector Slipping:**
  - Upon formatting, when bad sector $k$ is found, all sectors are slipped down by one index ($k \to k+1, k+1 \to k+2$). This maintains contiguous sector numbering, preventing head seek latency penalties.

---

## 3. Swap Space Architecture: Dedicated Partition vs Swap File

| Criteria | Dedicated Swap Partition (e.g. `/dev/sda2`) | Swap File (e.g. `/swapfile`) |
|---|---|---|
| **Allocation Mechanism** | Raw contiguous block allocation on raw disk slice | Regular file pre-allocated within filesystem via `fallocate` |
| **Filesystem Overhead** | **Zero.** Bypasses filesystem layer, inodes, and journaling | Traverses filesystem block maps (minimal in modern ext4/btrfs) |
| **Resizing Flexibility** | Very difficult; requires repartitioning, unmounting, or LVM | **Extremely flexible;** can expand or shrink dynamically on demand |
| **Multiple Storage Spread**| Can be placed across high-speed dedicated NVMe drives | Bound to the filesystem parent mount volume |

### Swap Space Sizing Decision for Hospital Server:
- For a hospital server with **64 GB RAM**:
  $$\text{Swap Size} = \mathbf{32\text{ GB} - 64\text{ GB}}$$
- Placed on a **dedicated mirrored NVMe swap partition** with `swappiness = 10` so Linux only pages during extreme burst peaks while ensuring maximum I/O throughput.

---

## 4. RAID Architecture Evaluation (6 Disks of 4 TB Each)

Raw Total Storage: $6 \times 4\text{ TB} = \mathbf{24\text{ TB}}$.

| Metric | RAID 0 | RAID 1 (Mirrored) | RAID 5 | RAID 6 | RAID 10 (1+0) |
|---|---|---|---|---|---|
| **Architecture** | Pure Striping | Disk Mirroring | Distributed Parity | Dual Distributed Parity | Striped Mirrors |
| **Usable Capacity** | **24.0 TB (100%)** | 12.0 TB (50%) | **20.0 TB (83.3%)** | **16.0 TB (66.7%)** | **12.0 TB (50.0%)** |
| **Fault Tolerance** | **0 Disks** (None) | 1 per pair | 1 Disk | **2 Any Disks** | **Up to 3 Disks** (1/pair) |
| **Write Penalty** | **1x** (No overhead) | 2x (2 writes) | **4x** (2 reads, 2 writes) | **6x** (3 reads, 3 writes) | **2x** (Mirrored write) |
| **Read Speedup** | $6\times$ | $6\times$ (balanced) | $5\times$ | $4\times$ | **$6\times$** |
| **Rebuild Risk** | N/A (Total loss) | Low | **High (URE vulnerability)**| Very Low | **Low (Fast rebuild)** |

---

## 5. Mathematical Reliability Model: Probability of Data Loss

Given:
- Annual Failure Rate (AFR) $p = 2\% = 0.02$.
- Mean Time to Repair / Array Rebuild Time $\tau = 24\text{ hours} = \frac{24}{8760}\text{ years} \approx 0.00274\text{ years}$.
- Probability of a drive failing during rebuild window:
  $$p_{\text{rebuild}} = p \times \tau = 0.02 \times \frac{24}{8760} \approx 5.48 \times 10^{-5}$$

### 5.1 Probability of Array Data Loss:
1. **RAID 1 (Mirrored Pair):**
   $$P_{\text{loss}}(\text{RAID 1}) = p \times p_{\text{rebuild}} = 0.02 \times (5.48 \times 10^{-5}) \approx \mathbf{1.096 \times 10^{-6}} \quad (\mathbf{1\text{ in } 912,500})$$
2. **RAID 5 (6 Disks):**
   After disk 1 fails, any of the remaining 5 disks failing during rebuild causes total array loss:
   $$P_{\text{loss}}(\text{RAID 5}) = N \cdot p \times (N-1) \cdot p_{\text{rebuild}} = 6(0.02) \times 5(5.48 \times 10^{-5}) \approx \mathbf{3.288 \times 10^{-5}} \quad (\mathbf{1\text{ in } 30,416})$$
3. **RAID 6 (6 Disks):**
   Requires **two additional disks** to fail during rebuild:
   $$P_{\text{loss}}(\text{RAID 6}) = 6(0.02) \times 5(p_{\text{rebuild}}) \times 4(p_{\text{rebuild}}) \approx \mathbf{7.21 \times 10^{-12}} \quad (\mathbf{1\text{ in } 138\text{ million}})$$

> **Critical Evaluation:** RAID 5 has a **$30\times$ higher probability of catastrophic data loss** than RAID 1/RAID 10 during rebuild, due to high rebuild stress and Unrecoverable Read Errors (URE).

---

## 6. Linux Disk Inspection Commands

On a production Linux hospital server:
```bash
# View block devices, partitions, sizes, and mountpoints
$ lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,LABEL

# View low-level partition table, disk identifiers, and geometry
$ sudo fdisk -l /dev/sda

# View active swap partitions/files and priority
$ swapon --show
```

---

## 7. Storage Configuration Recommendation for Hospital Records Server

**Recommended Configuration: RAID 10 (Striped Mirrors) on Enterprise NVMe SSDs with a Dedicated Mirrored Swap Partition.**

### Justification:
1. **Zero Rebuild Parity Penalty:** Hospital databases perform continuous random writes (patient vitals, lab orders, prescription logs). RAID 10 has a write penalty of only $2\times$ compared to $4\times$ in RAID 5 and $6\times$ in RAID 6.
2. **Rebuild Performance & Resilience:** If a disk fails in RAID 10, the rebuild is a simple raw block copy from its mirror partner (taking $<2$ hours on SSD). RAID 5/6 must read all surviving drives and recalculate XOR/Galois parity, crippling database throughput and risking URE failure.
3. **Capacity vs Safety:** While RAID 10 yields 12 TB (50% efficiency), 12 TB provides sufficient capacity for millions of patient records and imaging indexes, making absolute data durability and high write IOPS the top priority.

---

## 8. Alternative Concept & Complexity Analysis
**Alternative Concept:** Using **RAID 6** instead of RAID 5 or RAID 10.

### 1. Capacity:
- RAID 6 usable space: $(6 - 2) \times 4\text{ TB} = \mathbf{16\text{ TB}}$ (33% more capacity than RAID 10's 12 TB).

### 2. Parity Calculation & Write Penalty:
- RAID 6 computes **dual parity** ($P + Q$) using XOR and Galois Field ($GF(2^8)$) polynomial multiplication.
- A single small block write requires:
  $$\text{Read old data, read old } P, \text{ read old } Q, \text{ write new data, write new } P, \text{ write new } Q \implies \mathbf{6\text{ disk I/Os (Write Penalty = 6x)}}.$$
- During peak hospital admissions, RAID 6 creates heavy write latency bottlenecks on storage controllers.

### 3. Fault Survival:
- RAID 6 can survive **any 2 simultaneous drive failures**, providing mathematical protection ($P_{\text{loss}} \approx 7 \times 10^{-12}$) against double-disk collapse. For archival PACS image repositories (read-heavy), RAID 6 is ideal; but for transactional database workloads, RAID 10 remains superior.
