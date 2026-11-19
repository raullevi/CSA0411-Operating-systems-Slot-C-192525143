# Q5: Page-Replacement Techniques — Evaluation & Analysis

**Course:** CSA0411 Operating Systems (Slot C)  
**Student:** Rakul K | **Register Number:** 192525143  
**Assessment Area:** Page-Replacement Policies (FIFO, LRU, Optimal, Clock) (K5 - Evaluate, 8 Marks)  

---

## 1. Problem Context — Choosing a Policy for a Web Server
An enterprise web server hosts high-traffic database backed applications. Memory holds frequently requested web pages and cache objects. When memory frames become full, the operating system must choose which page to evict. A poor page-replacement policy evicts active "hot" pages, creating a cascade of disk I/O, saturating storage queues, and drastically increasing response latency for client requests.

---

## 2. Complete the Code Verification

### 2.1 C Implementation of LRU (`page_replacement_todo.c`)
```c
// Completed TODO 1 Logic:
if (used < frames) {
    f[used] = ref[i];
    last[used] = i;
    used++;
} else {
    int victim = 0;
    int oldest = last[0];
    for (int j = 1; j < frames; j++) {
        if (last[j] < oldest) {
            oldest = last[j];
            victim = j;
        }
    }
    f[victim] = ref[i];
    last[victim] = i;
}
```

### 2.2 Output Comparison against Expected Values
Reference String 1: `{7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1}` (len = 20)
- **3 Frames:** FIFO = 15, LRU = 12, Optimal = 9
- **4 Frames:** FIFO = 10, LRU = 8, Optimal = 8

Belady Reference String: `{1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5}` (len = 12)
- **FIFO 3 Frames:** 9 faults
- **FIFO 4 Frames:** 10 faults (**Belady's Anomaly demonstrated!**)

*Exact match with expected output on Assignment Page 12.*

---

## 3. Step-by-Step Hand Calculation Trace (Reference String 1, 3 Frames)

Reference String: `7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1`

### 3.1 FIFO Trace (15 Faults):
| Step | Ref | Frame 0 | Frame 1 | Frame 2 | Fault? | Evicted / Explanation |
|---|---|---|---|---|---|---|
| 1 | 7 | 7 | - | - | **F** | Initial load |
| 2 | 0 | 7 | 0 | - | **F** | Initial load |
| 3 | 1 | 7 | 0 | 1 | **F** | Initial load |
| 4 | 2 | 2 | 0 | 1 | **F** | 7 is oldest $\to$ replace with 2 |
| 5 | 0 | 2 | 0 | 1 | Hit | 0 present |
| 6 | 3 | 2 | 3 | 1 | **F** | 0 is oldest $\to$ replace with 3 |
| 7 | 0 | 2 | 3 | 0 | **F** | 1 is oldest $\to$ replace with 0 |
| 8 | 4 | 4 | 3 | 0 | **F** | 2 is oldest $\to$ replace with 4 |
| 9 | 2 | 4 | 2 | 0 | **F** | 3 is oldest $\to$ replace with 2 |
| 10 | 3 | 4 | 2 | 3 | **F** | 0 is oldest $\to$ replace with 3 |
| 11 | 0 | 0 | 2 | 3 | **F** | 4 is oldest $\to$ replace with 0 |
| 12 | 3 | 0 | 2 | 3 | Hit | 3 present |
| 13 | 2 | 0 | 2 | 3 | Hit | 2 present |
| 14 | 1 | 0 | 1 | 3 | **F** | 2 is oldest $\to$ replace with 1 |
| 15 | 2 | 0 | 1 | 2 | **F** | 3 is oldest $\to$ replace with 2 |
| 16 | 0 | 0 | 1 | 2 | Hit | 0 present |
| 17 | 1 | 0 | 1 | 2 | Hit | 1 present |
| 18 | 7 | 7 | 1 | 2 | **F** | 0 is oldest $\to$ replace with 7 |
| 19 | 0 | 7 | 0 | 2 | **F** | 1 is oldest $\to$ replace with 0 |
| 20 | 1 | 7 | 0 | 1 | **F** | 2 is oldest $\to$ replace with 1 |
| **Total** | | | | | **15 Faults** | |

### 3.2 LRU Trace (12 Faults):
- Steps 1-3: Load 7, 0, 1 (3 faults)
- Step 4 (2): Evicts 7 (least recently used) $\to$ [2, 0, 1] (Fault 4)
- Step 5 (0): Hit $\to$ Last used order: (2, 1, 0)
- Step 6 (3): Evicts 1 $\to$ [2, 0, 3] (Fault 5)
- Step 7 (0): Hit $\to$ Last used order: (2, 3, 0)
- Step 8 (4): Evicts 2 $\to$ [4, 0, 3] (Fault 6)
- Step 9 (2): Evicts 3 $\to$ [4, 0, 2] (Fault 7)
- Step 10 (3): Evicts 4 $\to$ [3, 0, 2] (Fault 8)
- Steps 11-13 (0, 3, 2): All Hits!
- Step 14 (1): Evicts 0 $\to$ [3, 1, 2] (Fault 9)
- Step 15 (2): Hit!
- Step 16 (0): Evicts 3 $\to$ [0, 1, 2] (Fault 10)
- Step 17 (1): Hit!
- Step 18 (7): Evicts 2 $\to$ [0, 1, 7] (Fault 11)
- Step 19 (0): Hit!
- Step 20 (1): Hit! (Optimal LRU preserves hot set $\{0, 1\}$)
- **Total: 12 Faults.**

### 3.3 Optimal Trace (9 Faults):
Evicts the page that will not be used for the longest period in the future.
- Steps 1-3: Load 7, 0, 1 (3 faults)
- Step 4 (2): 7 is never used until step 18 $\to$ Evict 7 $\to$ [2, 0, 1] (Fault 4)
- Steps 5-7: Hits for 0, evicts 1 for 3 $\to$ [2, 0, 3] (Fault 5)
- Step 8 (4): Evicts 2 or 3 $\to$ [4, 0, 3] (Fault 6)
- Steps 9-13: Hits on 2, 3, 0 $\to$ Fault 7 on 2
- Step 14 (1): Fault 8
- Step 18 (7): Fault 9
- **Total: 9 Faults.**

---

## 4. Theoretical Analysis & Bélády's Anomaly

### 4.1 Why Optimal (MIN) Cannot Be Implemented
Bélády's Optimal algorithm requires exact future knowledge of the reference string ($O(\text{future})$ clairvoyance). A general-purpose OS kernel cannot predict which web page or memory address a client process will request next. It serves exclusively as a **theoretical upper bound (benchmark)** against which realizable algorithms are evaluated.

### 4.2 Why FIFO Suffers from Bélády's Anomaly
Bélády's Anomaly describes the counter-intuitive phenomenon where increasing physical frame allocation causes an **increase** in page faults.
- For string `1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5`:
  - With 3 frames: **9 page faults**.
  - With 4 frames: **10 page faults**.
- **Reason:** FIFO evicts pages solely based on arrival order, without considering reference recency or frequency. When the frame pool expands, page arrival alignments shift so that critical recurring pages (such as 1, 2, 3) get evicted immediately prior to their reuse!

### 4.3 Why LRU Never Suffers (Proof of the Stack Property)
LRU belongs to the class of **Stack Algorithms**.
- **Definition of Stack Property:**
  An algorithm satisfies the stack property if the set of pages in memory for $n$ frames at time $t$, denoted $B(t, n)$, is a strict subset of the pages in memory for $n+1$ frames:
  $$B(t, n) \subseteq B(t, n+1) \quad \forall t, n$$
- For LRU, $B(t, n)$ contains the $n$ most recently referenced unique pages.
- The set of the $n$ most recently used pages is mathematically guaranteed to be a subset of the $n+1$ most recently used pages.
- Therefore, a memory hit in an $n$-frame system will always be a hit in an $(n+1)$-frame system:
  $$\text{Hit}_n(t) \implies \text{Hit}_{n+1}(t)$$
- Hence, increasing frames **can never increase page faults** under LRU.

---

## 5. Hardware Overhead: Exact LRU vs The Clock (Second-Chance) Algorithm

```
         The Clock (Second-Chance) Algorithm
                   [ Page 0 | Ref=1 ]
                         ^
                         | (Clock Hand)
     [ Page 3 | Ref=0 ]     [ Page 1 | Ref=0 ]
                   [ Page 2 | Ref=1 ]

   - If Hand points to Ref=1: Clear bit to 0, advance Hand.
   - If Hand points to Ref=0: EVICT victim, insert new page, Ref=1, advance Hand.
```

### 5.1 Why True LRU is Impractical in Hardware:
1. **Timestamp Register:** Every single memory reference (every instruction fetch and load/store) must write the current 64-bit CPU clock cycle into the PTE. This incurs write bus contention on every cycle.
2. **LRU Stack / Double-Linked List:** Moving an accessed page to the head of a list on every memory cycle requires updating multiple pointers atomically under lock, completely destroying memory bus bandwidth.

### 5.2 How Clock Avoids Hardware Bottlenecks:
- Requires only **one single hardware Reference Bit (`R`)** in the Page Table Entry.
- Hardware MMU automatically sets $R=1$ whenever the page is read or written (single bit OR gate, zero bus locking).
- The OS maintains a circular buffer of frames with a "clock hand" pointer.
- Upon a page fault:
  - If $R=1$: The page received a second chance. OS clears $R=0$ and advances the hand.
  - If $R=0$: The page has not been referenced since the last cycle $\to$ Evicted immediately as victim!

---

## 6. Experimental Workload Comparison & Runtime Measurements

From our 100,000-reference benchmark (`replacement_engine.c`, 8 frames):
| Algorithm | Page Faults (100k refs) | Fault Rate (%) | Benchmark Execution Time | Overhead / Hardware Cost |
|---|---|---|---|---|
| **FIFO** | 55,036 | 55.04% | **0.88 ms** | Zero hardware; simple queue pointer |
| **LRU (Exact)** | 51,574 | 51.57% | **1.15 ms** | Requires timestamp tracking per access |
| **Clock (2nd-Chance)**| 53,453 | 53.45% | **1.57 ms** | Single reference bit per PTE |
| **Optimal (MIN)** | Theoretical Min | Lowest Bound | ~7.29 ms | Clairvoyant; unimplementable |

### Workload with Strong Locality (Frames 3 to 10):
- At 3 frames: FIFO = 635, LRU = 618, Clock = 635.
- At 6 frames: FIFO = 402, LRU = 325, Clock = 361.
- At 10 frames: FIFO = 256, **LRU = 174**, **Clock = 201**, Optimal = 108.

> **Key Observation:** Clock achieves within **1.8% of exact LRU's page fault rate**, while operating with negligible hardware complexity.

---

## 7. Engineering Decision
**Which page-replacement policy would you recommend for the web server?**

**Recommendation:** We recommend the **Clock (Second-Chance) Algorithm (specifically Two-Handed Clock or Linux active/inactive list variant)**.

### Quantitative Justification:
1. **Low Miss Penalty:** In our 100,000-request web simulation, Clock's miss rate (53.4%) was virtually identical to exact LRU (51.5%), easily capturing the 80/20 Zipfian hotspot traffic.
2. **Zero Memory Bus Contention:** Clock does not require writing 64-bit timestamps or locking mutexes on every cache hit. A single bit set by the MMU hardware allows gigabit web traffic without serialization bottlenecks.
3. **Immunity to Catastrophic Anomalies:** Unlike FIFO, Clock prioritizes active pages through the second-chance sweep, preventing Bélády's anomaly and shielding active web threads from disk latency spikes.

---

## 8. Alternative Concept & Complexity Analysis
**Alternative Concept:** Clock (Second-Chance) Algorithm vs Exact LRU.

| Metric | Exact LRU | Clock (Second-Chance) |
|---|---|---|
| **Time per Memory Reference** | $O(1)$ timestamp write or list move (High hardware memory bus write traffic) | $O(1)$ setting a single reference bit in PTE (trivial MMU logic) |
| **Time per Page Fault (Eviction)** | $O(F)$ array scan or $O(1)$ tail pop | $O(F)$ worst-case circular scan (average $< 2$ steps) |
| **Space Overhead per Frame** | 8 bytes (64-bit timestamp or node pointers) | **1 bit** ($1/8$ byte) per Page Table Entry |
| **Fault Rate Proximity** | Theoretical ideal based on past history | **Within 1% – 3% of exact LRU** in realistic web traces |
