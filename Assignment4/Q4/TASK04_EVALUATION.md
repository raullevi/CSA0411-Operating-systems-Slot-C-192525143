# Task 4: Disk Scheduling Algorithms

**Course:** CSA04 / CSA0411 – Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Task 4.1: Mathematical Calculation of Head Movement (Cylinders 0–199, Initial Head = 53)
Request Queue: $\{98, 183, 37, 122, 14, 124, 65, 67\}$

### 1. First-Come, First-Served (FCFS):
- Order: $53 \to 98 \to 183 \to 37 \to 122 \to 14 \to 124 \to 65 \to 67$
- Movement: $|98-53| + |183-98| + |37-183| + |122-37| + |14-122| + |124-14| + |65-124| + |67-65|$
  $$= 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = \mathbf{640 \text{ cylinders}}$$

### 2. Shortest Seek Time First (SSTF):
- Order: $53 \to 65 \to 67 \to 37 \to 14 \to 98 \to 122 \to 124 \to 183$
- Movement: $(67 - 53) + (67 - 14) + (183 - 14) = 14 + 53 + 169 = \mathbf{236 \text{ cylinders}}$

### 3. SCAN (Elevator Algorithm towards Cylinder 0 First):
- Order: $53 \to 37 \to 14 \to 0 \to 65 \to 67 \to 98 \to 122 \to 124 \to 183$
- Movement: $(53 - 0) + (183 - 0) = 53 + 183 = \mathbf{236 \text{ cylinders}}$

### 4. Circular SCAN (C-SCAN towards Cylinder 199 First):
- Order: $53 \to 65 \to 67 \to 98 \to 122 \to 124 \to 183 \to 199 \xrightarrow{\text{jump}} 0 \to 14 \to 37$
- Movement: $(199 - 53) + (37 - 0) = 146 + 37 = \mathbf{183 \text{ cylinders (+199 for the return jump)}}$

### 5. LOOK:
- Order: $53 \to 37 \to 14 \to 65 \to 67 \to 98 \to 122 \to 124 \to 183$
- Movement: $(53 - 14) + (183 - 14) = 39 + 169 = \mathbf{208 \text{ cylinders}}$

### 6. Circular LOOK (C-LOOK):
- Order: $53 \to 65 \to 67 \to 98 \to 122 \to 124 \to 183 \xrightarrow{\text{jump}} 14 \to 37$
- Movement: $(183 - 53) + (37 - 14) = 130 + 23 = \mathbf{153 \text{ cylinders (+169 for jump)}}$

---

## 2. Task 4.2 & 4.3: Fairness, Starvation, and C-SCAN Uniformity

### Why SSTF Causes Severe Starvation:
- SSTF greedily serves requests nearest to the current head position.
- In our simulation, when a continuous stream of requests arrives near cylinder 60, the disk head oscillates indefinitely between cylinders 58 and 62.
- The pending request at cylinder 183 is **never served (infinite starvation)**.

### Why C-SCAN Provides More Uniform Waiting Time Than SCAN:
- In SCAN, when the head reverses direction at cylinder 0 and sweeps outward, the cylinders immediately behind it (e.g., 5 to 20) have just been serviced and have minimal new requests. The cylinders at the far end (180 to 199) have been waiting the longest.
- C-SCAN treats cylinders as a circular ring: upon reaching cylinder 199, it immediately returns to cylinder 0 without servicing requests on the return sweep. This ensures that every cylinder experiences an identical, predictable maximum waiting interval.

---

## 3. Task 4.4: Solid-State Drives (SSDs) and the `none` / `mq-deadline` Schedulers
- Solid-State Drives have **zero mechanical read-write heads, zero track seek latency, and zero rotational delay**.
- Arranging I/O requests by physical logical block address (LBA) on SSDs provides zero hardware performance gain. Instead, traditional elevator algorithms waste CPU cycles sorting queues and introduce mutex lock contention on multi-core servers.
- Linux assigns `none` (noop / bypass) or `mq-deadline` (multi-queue deadline) to NVMe/SATA SSDs. This ensures fast FIFO dispatch with minimal software overhead while enforcing simple read/write starvation deadlines.

---

## 4. Complete the Code Verification: `disk_sched_todo.c`

```c
// Completed TODO 1 logic (SSTF Selection):
int best_idx = -1;
int min_dist = 999999;
for (int i = 0; i < N; i++) {
    if (!done[i]) {
        int dist = abs(req[i] - pos);
        if (dist < min_dist) {
            min_dist = dist;
            best_idx = i;
        }
    }
}
done[best_idx] = 1;
order[k] = req[best_idx];
pos = req[best_idx];
```

### Execution Output (Character-for-Character Exact Match):
```
FCFS   53 98 183 37 122 14 124 65 67 -> 640 cylinders
SSTF   53 65 67 37 14 98 122 124 183 -> 236 cylinders
SCAN   53 37 14 0 65 67 98 122 124 183 -> 236 cylinders
C-SCAN 53 65 67 98 122 124 183 199, jump to 0 14 37 -> 183 cylinders (+199 for the jump)
```
