# Task 5: Distributed and Cloud-Based Storage

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task 5.1: Distributed & Cloud Storage Comparison Matrix

| Storage Architecture | Consistency Model | High Availability Strategy | Read/Write Latency | Cost Scaling Model | Target University Workload |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **Network File System (NFS)** | Close-to-Open (Weak / Inconsistent during concurrent writes) | **Low** (Single NFS server is SPOF without HA clustering) | **Low** ($< 2\,\text{ms}$ on local LAN) | Expensive enterprise NAS storage | Campus engineering computer labs |
| **Distributed FS (Ceph / HDFS)** | **Strong Consistency** (POSIX compliant in CephFS) | **Exceptional** (Automated rack-aware node failover) | Medium ($5-15\,\text{ms}$) | Commodity x86 servers with JBOD disks | University research datasets, VM disks |
| **Cloud Object Storage (S3 / GCS)** | **Strong Consistency** (Read-after-write for new objects) | **Maximum** ($99.999999999\%$ 11 9's durability) | High ($50-120\,\text{ms}$ over Internet) | Pay-as-you-go per GB + egress fees | Student home submissions, long-term archives |

---

## 2. Task 5.2: Replication, Fault Tolerance & The Consistency Trade-Off

### How 3-Way Replication Protects Data:
In distributed file systems like HDFS and Ceph, every data block is replicated across **three separate storage nodes**:
- **Replica 1:** Local rack on the node where the client writes.
- **Replica 2:** Different node on the same local rack (protects against node power supply failure).
- **Replica 3:** Different node on an independent remote rack (protects against top-of-rack network switch failure).
- If any drive or storage server crashes, the Ceph CRUSH algorithm automatically identifies degraded placement groups and spawns background re-replication without service disruption.

### Strong vs. Eventual Consistency (CAP Theorem):
- **Strong Consistency (CP System):** Every write must be synchronously acknowledged by a majority quorum (e.g., $W + R > N$). Guarantees that every subsequent read immediately reflects the latest update (essential for student grade submission ledgers). Trade-off: Higher write latency and reduced availability during network partition.
- **Eventual Consistency (AP System):** Writes are acknowledged asynchronously on the local replica and propagated to peers in the background. If a network partition occurs, replicas diverge temporarily. Once partitions heal, conflict resolution (vector clocks / last-write-wins) reconverges data. Optimal for high-throughput video viewing metrics.

---

## 3. Task 5.3: Operating System Device Management for Storage
The operating system abstracts heterogeneous storage controllers through standard layers:
1. **Device Drivers:** Translate high-level POSIX block read/write commands into controller-specific register operations (e.g., AHCI SATA registers, NVMe submission/completion queues).
2. **Buffering:** Intermediate kernel memory buffers that decouple producer write bursts from slower physical disk write latencies.
3. **Page Caching:** Transparently keeps recently accessed disk blocks in unallocated physical RAM. Subsequent reads hit RAM ($100\,\text{ns}$) rather than disk ($10\,\text{ms}$).
4. **Spooling:** Queues concurrent print or batch transmission streams in intermediate disk files to serialize output onto exclusive non-shareable devices.
5. **Block vs. Character Interface:** Block devices (`/dev/sda`, `/dev/nvme0n1`) transfer fixed-size blocks ($4\,\text{KB}$) with random seeking and caching. Character devices (`/dev/tty`, `/dev/urandom`) stream unbuffered sequential byte streams.

---

## 4. Alternative Concept & Complexity Analysis: Central NFS Server vs. Replicated Ceph

If the university used a single monolithic NFS server instead of Ceph:
- **Scalability Limit:** As active students scale from 1,000 to 12,000, NFS network queue depth and socket lock contention collapse I/O throughput to $< 10 \text{ MB/s}$.
- **Availability Risk:** A single motherboard or power outage on the NFS head node renders all student home folders across all campuses completely inaccessible. Ceph distributes I/O across 50 commodity storage nodes, surviving simultaneous loss of multiple server racks.
