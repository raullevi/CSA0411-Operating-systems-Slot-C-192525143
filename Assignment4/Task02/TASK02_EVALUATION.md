# Task 2: From Workload to File-Allocation Method

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task 2.1: Workload & Operations Analysis (Video Surveillance NVR)
A network video recorder (NVR) ingests live streams from 32 high-definition security cameras:
- **Write Workload (Append-Only):** Continuous, predictable stream of encoded video packets ($2-8\,\text{Mbps}$ per camera). Files grow monotonically over 24 hours.
- **Read Workload (Hybrid Access):**
  - *Sequential Read:* Forensics playback reviewing hours of continuous footage.
  - *Direct / Random Access Seek:* Timestamp-based incident search (jumping directly to a specific minute/second).
- **Deletion Pattern (FIFO Bulk Purge):** Full 24-hour video container files are unlinked after 30 days of retention to reclaim disk space.

---

## 2. Task 2.2: Comparison of File Allocation Methods

| Allocation Method | Sequential Access Speed | Direct / Random Seek Speed | File Growth Flexibility | External Fragmentation | Reliability & Fault Tolerance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Contiguous Allocation** | **Maximum** (Zero head seek; sequential sectors) | **$O(1)$** (Direct arithmetic offset calculation) | **Terrible** (Must declare max file size upfront; fails if adjacent blocks full) | **Severe** (Disk becomes checkerboard of unusable gaps) | Moderate (Corrupted sector damages only local data) |
| **Linked Allocation (Embedded)** | High (Follow disk pointer block-by-block) | **$O(K)$** (Must read all $K-1$ previous disk blocks) | **Excellent** (Append any free block anywhere) | **Zero** (Any free block can be utilized) | **Terrible** (Single bad pointer breaks entire remainder of file) |
| **Linked Allocation (FAT)** | High (Sequential block traversal) | **Moderate** (Traverse linked list in RAM FAT table) | **Excellent** (Dynamically allocate free clusters) | **Zero** (Scattered clusters linked via table) | Moderate (Damaged FAT file table loses entire disk mapping) |
| **Indexed Allocation (Inode)** | High (Index cache prefetching) | **$O(1)$ to $O(3)$** (Index pointer indirection) | **Outstanding** (Append dynamic index blocks on demand) | **Zero** (Any free data block can be indexed) | **High** (Inodes + block pointers backed by journaling) |

---

## 3. Task 2.3: Mathematical Cost & Capacity Calculations

### A. Number of Disk Reads to Reach the Last Block of a 4 GB File (4 KB Blocks)
- Total Data Blocks = $\frac{4\,\text{GB}}{4\,\text{KB}} = \frac{4 \times 1024 \times 1024\,\text{KB}}{4\,\text{KB}} = \mathbf{1,048,576 \text{ blocks}}$ ($2^{20}$ blocks).
- **1. Contiguous Allocation:**
  $$\text{Disk Reads} = \mathbf{1 \text{ read}}$$
  The OS computes the physical sector address in CPU registers: $\text{LBA}_{\text{target}} = \text{Start} + 1,048,575$ and issues a single direct disk seek.
- **2. Standard Linked Allocation (Pointers inside data blocks):**
  $$\text{Disk Reads} = \mathbf{1,048,576 \text{ reads}}$$
  The head must sequentially read every preceding block to extract the address of the next block.
- **3. Linked Allocation with In-Memory FAT:**
  $$\text{Disk Reads} = \mathbf{1 \text{ read}}$$
  The entire cluster chain is traversed in RAM inside the FAT cache; only the final target data block is fetched from disk.
- **4. Indexed Allocation (UNIX Inode with 4-byte block pointers):**
  - Direct blocks: $12 \text{ blocks}$.
  - Single-indirect block holds: $\frac{4096}{4} = 1,024 \text{ pointers}$.
  - Double-indirect block holds: $1024 \times 1024 = 1,048,576 \text{ pointers}$.
  - Block index $1,048,575$ resides in the **Double-Indirect block**.
  - Total Disk Reads = 1 (read double-indirect table) + 1 (read secondary index block) + 1 (read actual data block) = **$\mathbf{3 \text{ disk reads}}$** (assuming cold cache).

### B. Maximum File Size Supported by the Inode Architecture
- Direct blocks: $12 \times 4\,\text{KB} = 48\,\text{KB}$
- Single-indirect: $1024 \times 4\,\text{KB} = 4,096\,\text{KB} = 4\,\text{MB}$
- Double-indirect: $1024 \times 1024 \times 4\,\text{KB} = 1,048,576 \times 4\,\text{KB} = 4\,\text{GB}$
- Triple-indirect: $1024 \times 1024 \times 1024 \times 4\,\text{KB} = 1,073,741,824 \times 4\,\text{KB} = \mathbf{4\,\text{TB}}$
$$\text{Total Max File Size} = 48\,\text{KB} + 4\,\text{MB} + 4\,\text{GB} + 4\,\text{TB} \approx \mathbf{4.004\,\text{TB}}$$

---

## 4. Task 2.4: Free-Space Management Comparison for a 4 TB Disk

- Total blocks on a $4\,\text{TB}$ disk ($4\,\text{KB}$ block size) = $\frac{4 \times 10^{12}}{4096} = 2^{30} \text{ blocks} = \mathbf{1,073,741,824 \text{ blocks}}$.
- **Bit Vector Size Calculation:**
  $$\text{Size} = \frac{1,073,741,824 \text{ bits}}{8 \text{ bits/byte}} = 134,217,728 \text{ bytes} = \mathbf{128\,\text{MB}}$$
  *Evaluation:* Storing $128\,\text{MB}$ in RAM is trivial for modern servers and allows hardware word-scanning (`__builtin_ffs`) for instant $O(1)$ free-block allocation.
- **Linked Free List:** Eliminates continuous RAM consumption by storing pointers inside free blocks, but traversing scattered free blocks during multi-block allocation generates severe head movement.
- **Grouping & Counting:** Keeps count of consecutive free blocks (extents). For an NVR where files are purged in 24-hour batches, **extent-based grouping** is the most efficient, reducing metadata footprint by over $99\%$.

---

## 5. Complete the Code Verification: `file_alloc_todo.c`

```c
// Completed TODO 1 logic (First-Fit Contiguous Allocation):
int count = 0, start = -1;
for (int i = 0; i < BLOCKS; i++) {
    if (disk[i] == '.') {
        if (count == 0) start = i;
        count++;
        if (count == size) {
            for (int j = start; j < start + size; j++) {
                disk[j] = file;
            }
            return start;
        }
    } else {
        count = 0;
        start = -1;
    }
}
return -1;
```

### Execution Output (Character-for-Character Exact Match):
```
AAAAAA........CCCCC.............
E (10 blocks) contiguous: start 19
E (10 blocks) indexed: index block 6, data blocks 7 8 9 10 11 12 13 29 30 31
AAAAAAeEEEEEEECCCCCEEEEEEEEEEEEE
```

---

## 6. Alternative Concept & Complexity Analysis: File Allocation Table (FAT) vs. Inode

If the NVR used a File Allocation Table (FAT32) held in RAM:
- **Time Complexity for Random Seek ($K$):** Traversing to block $K$ in FAT requires chasing $K$ pointer entries in memory ($O(K)$ CPU operations). For a 4 GB file ($10^6$ blocks), seeking takes thousands of memory dereferences, compared to $O(1)$ three-level index lookups in an Inode.
- **Memory Footprint of FAT Table for 4 TB Disk:** Each FAT entry requires 4 bytes. For $2^{30}$ blocks, the FAT table consumes:
  $$\text{FAT Table RAM} = 1,073,741,824 \times 4 \text{ bytes} = \mathbf{4\,\text{GB RAM}}$$
  Permanently pinning $4\,\text{GB}$ of physical RAM solely for the FAT file table is severely wasteful on embedded NVR hardware.
- **Reliability Risk:** If a sudden power loss occurs during recording, corruption of the central FAT table invalidates directory chains for all 32 cameras simultaneously.

> **Design Recommendation:** Deploy **Extent-Based Indexed Allocation (XFS or ext4 with extents)** for the NVR storage engine.
