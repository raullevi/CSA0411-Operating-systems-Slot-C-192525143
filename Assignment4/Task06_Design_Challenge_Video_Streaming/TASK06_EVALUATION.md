# Task 6: Design Challenge – Storage Architecture for a Video-Streaming Start-up

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Stage 1: Interpret the Workload & Performance Targets
A video-streaming platform delivers university lectures to **200,000 active students**:
- **Video Catalog Characteristics:** Each lecture video is $300\,\text{MB}$ to $2\,\text{GB}$ in MP4/H.264 format. Uploaded once (immutable write-once asset).
- **Access Skew (80/20 Pareto Locality):** Videos are viewed thousands of times during the first 7 days following release ("Hot Tier"), after which viewing frequency drops by $> 95\%$ ("Cold Tier").
- **Random Seeking Pattern:** Students jump to arbitrary minutes/timestamps during revision.
- **Measurable SLAs:**
  1. Initial playback start latency $\le 200\,\text{ms}$.
  2. Timestamp seek buffering latency $\le 300\,\text{ms}$.
  3. Zero playback buffering pauses for 10,000 concurrent peak streams.

---

## 2. Stage 2: Proposed Multi-Tier Storage Architecture

```
[200,000 Students Worldwide]
             |
             v
   +--------------------+
   |  Cloud CDN Edge    | (Cloudflare / CloudFront Edge Cache)
   +--------------------+
             | (Cache Miss: 10%)
             v
   +-------------------------------------------------------------+
   |              ON-PREMISE STREAMING ORIGIN SERVERS            |
   |                                                             |
   |  +-------------------------------------------------------+  |
   |  | TIER 1 (HOT CACHE): High-Speed PCIe Gen4 NVMe SSDs    |  |
   |  | - Holds Week-1 Releases & HLS Playlist Manifests      |  |
   |  | - Block size: 1 MB chunks | Scheduler: 'none' (noop)  |  |
   |  +-------------------------------------------------------+  |
   |                             | (LRU Eviction after 7 Days)   |
   |                             v                               |
   |  +-------------------------------------------------------+  |
   |  | TIER 2 (COLD ARCHIVE): High-Capacity SATA 7200RPM HDDs|  |
   |  | - Holds Historical Scans & Archived Lectures (200 TB) |  |
   |  | - Software RAID 6 Array | Scheduler: BFQ / C-SCAN     |  |
   |  +-------------------------------------------------------+  |
   +-------------------------------------------------------------+
```

---

## 3. Stage 3: Critical Operating System & Storage Decisions
- **Block Size (1 MB to 2 MB Extents):** Videos are transcoded into HTTP Live Streaming (HLS) / MPEG-DASH chunks of 2 seconds each ($\approx 1-2\,\text{MB}$ per chunk). Matching file-system block allocation directly to media segment size eliminates internal fragmentation and enables single-read seek dispatch.
- **I/O Scheduler:**
  - NVMe SSD Tier: Configured with `none` (noop) to bypass elevator sorting and exploit parallel hardware submission queues.
  - SATA HDD Tier: Configured with `mq-deadline` or `BFQ` to prevent disk head thrashing during concurrent read requests.
- **Replication Strategy:** On-premise storage uses **RAID 6 (Dual Parity)** to survive simultaneous loss of two mechanical drives, paired with an asynchronous background backup to Amazon S3 Glacier.

---

## 4. Stage 4: Design Calculations

### A. Number of Disk Reads to Start Playing at Any Minute:
Using HLS chunking:
1. Student clicks timestamp 34:12.
2. The client fetches the `.m3u8` index playlist file (**1 disk read**).
3. The manifest maps 34:12 to `segment_1026.ts` ($1.2\,\text{MB}$).
4. The server directly seeks to the physical extent of `segment_1026.ts` (**1 disk read**).
$$\text{Total Disk Reads to Start Playback} = \mathbf{2 \text{ disk reads}}$$

### B. Throughput & Server Capacity:
- Each 1080p stream requires $2.5\,\text{Mbps} = 0.3125\,\text{MB/s}$.
- A PCIe Gen4 x4 NVMe SSD delivers $7,000\,\text{MB/s}$ read bandwidth.
$$\text{Max Concurrent Streams per SSD} = \frac{7000\,\text{MB/s}}{0.3125\,\text{MB/s}} \approx \mathbf{22,400 \text{ concurrent streams}}$$
A cluster of four NVMe origin servers comfortably sustains all 200,000 students without bottlenecking.

---

## 5. Stage 5: Empirical Simulation & Comparison (Design A vs. Design B)

Results from `video_storage_sim`:

| Metric / Measurement | Design A (Monolithic HDD) | Design B (Tiered NVMe SSD + HDD) | Performance Impact |
| :--- | :---: | :---: | :--- |
| **NVMe Cache Hit Rate** | $0.00\%$ (No SSD Tier) | **$80.04\%$** | $80\%$ of traffic served from flash |
| **Average Playback Seek Latency** | $8.50\,\text{ms}$ | **$1.74\,\text{ms}$** | **$4.9\times$ Latency Reduction** |
| **Max Concurrent Streams / Server** | $\approx 120$ streams (Head Seek Cap) | **$\approx 8,500+$ streams** | **$70\times$ Higher Concurrency** |

---

## 6. Alternative Concept & Complexity Analysis: Pure Cloud S3 + CloudFront CDN

If the company used 100% cloud object storage and a global CDN instead of on-premise tiered servers:
- **Playback Latency for Global Students:** Cloudflare/CloudFront caches segments at edge points of presence (PoPs) within $15\,\text{ms}$ of students, delivering superior worldwide streaming speed.
- **Egress Cost Explosion:** Delivering 200,000 streams at 50 GB/student/month equals $10\,\text{Petabytes/month}$. Cloud egress at $\$0.05/\text{GB}$ costs **$\$500,000/\text{month}$**, bankrupting an early-stage startup!
- **Recommended Verdict:** Adopt **Hybrid Architecture**: On-premise NVMe/HDD servers act as high-volume zero-cost local origin; free-tier/low-cost Cloudflare CDN caches top 5% viral video manifests at the edge.
