# Task 08: Evaluate CPU States and Protection

**Course:** CSA0411 / CSA04 - Operating Systems (Slot C)  
**Student Name:** Rakul K  
**Register Number:** 192525143  
**Institution:** SIMATS Engineering, Saveetha University  
**Bloom's Taxonomy Level:** K5 – Evaluate  

---

## 1. Dual-Mode Operation & Hardware Privilege Rings
To protect the operating system and life-critical patient monitoring devices from erratic user code, CPUs implement hardware-enforced privilege modes:
- **Kernel Mode (Supervisor / Ring 0):** Full access to all hardware instructions, control registers (CR0, CR3, CR4 on x86; SCTLR_EL1 on ARM), page table mappings, and interrupt disable instructions (`CLI` / `STI`).
- **User Mode (Ring 3):** Restricted execution mode. Attempting to execute privileged instructions triggers a General Protection Fault (`#GP`), instantly halting the errant process.
- **The Mode Bit:** A hardware flag in the processor status register (e.g. `CPL` bits in `CS` register) indicates whether the CPU is operating in User (1) or Kernel (0) mode.

---

## 2. Timer Interrupts & Preventing Infinite Loops
- In early batch systems without hardware timers, an infinite loop in a program permanently seized the CPU, requiring physical power resets.
- Modern OS kernels program a hardware timer chip (e.g. LAPIC / ARM Generic Timer) to fire periodic interrupts every $1-10\,\text{ms}$.
- When the timer interrupt fires, the CPU forces a mode switch into Ring 0, executing the kernel scheduler ISR. If a patient monitor task runs longer than its allotted quantum, the kernel preempts it, ensuring life-critical ECG heart rate alarms are serviced within the mandated $10\,\text{ms}$ threshold.

---

## 3. Disabling Interrupts & Life-Critical Safety
- If arbitrary user programs on a bedside monitor could execute privileged `CLI` (Clear Interrupt Flag) instructions:
  - An errant diagnostic app could disable interrupts and enter a loop.
  - The hardware ADC timer interrupts from the cardiac sensor would be masked.
  - The patient enters cardiac arrest, but the monitor is silenced because interrupt lines are blocked!
- **Hardware Protection:** `CLI` is strictly a privileged Ring 0 instruction. In User Mode, executing `CLI` triggers `SIGSEGV` or `#GP`, terminating the rogue process immediately.

---

## 4. Alternative Concept & Complexity Analysis: Polling vs. Interrupt-Driven I/O for Monitors

If the bedside monitors used **busy-wait polling** (checking the sensor in a loop) instead of hardware interrupts:
1. **Worst-Case Detection Latency:**  
   If the polling loop samples every $50\,\text{ms}$, an acute ventricular arrhythmia occurring right after a sample is ignored for $50\,\text{ms}$, violating the $\le 10\,\text{ms}$ safety SLA.
2. **CPU & Power Waste:**  
   Polling burns $100\%$ CPU utilization running tight loops reading memory addresses, generating excessive thermal heat and draining backup battery power within 45 minutes during mains power failure.
3. **Interrupt Efficiency:**  
   With hardware interrupts, the CPU sleeps in deep low-power state (`HLT` / `WFI`) drawing $< 50\,\text{mW}$, waking instantaneously ($< 2\,\mu\text{s}$) upon hardware sensor threshold trip.
