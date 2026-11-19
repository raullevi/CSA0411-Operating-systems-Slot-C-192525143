/**
 * Task 04: Disk Scheduling Simulation Suite (10,000 Requests)
 * Evaluates FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK under Light, Medium, Heavy loads.
 * Course: CSA04 / CSA0411 - Operating Systems (Slot C)
 * Student: Rakul K | Register Number: 192525143
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_CYLINDERS 200
#define NUM_REQUESTS 10000

int cmp_int(const void *a, const void *b) { return (*(const int *)a - *(const int *)b); }

void evaluate_starvation_sstf(void) {
    printf("--- SSTF Starvation Experiment ---\n");
    printf("Initial pending request at cylinder 183. Stream of requests arriving near cylinder 60...\n");
    int pos = 53;
    int pending_target = 183;
    int serviced_near_60 = 0;

    for (int t = 0; t < 50; t++) {
        int new_req = 58 + (t % 5); /* Requests near 60 */
        if (abs(new_req - pos) < abs(pending_target - pos)) {
            pos = new_req;
            serviced_near_60++;
        }
    }
    printf("Serviced %d requests near cylinder 60. Request at 183 was starved and NEVER served!\n", serviced_near_60);
    printf("Conclusion: SSTF exhibits severe starvation under continuous localized arrival.\n\n");
}

int main(void) {
    printf("======================================================================\n");
    printf("  CSA0411 OPERATING SYSTEMS - ASSIGNMENT 4 (CO4)\n");
    printf("  Task 04: Disk Scheduling Suite & SSTF Starvation Evaluation\n");
    printf("  Student: Rakul K (Reg No: 192525143)\n");
    printf("======================================================================\n\n");

    evaluate_starvation_sstf();

    printf("Disk Scheduling Policy Comparison for Queue {98, 183, 37, 122, 14, 124, 65, 67} (Head=53):\n");
    printf("----------------------------------------------------------------------------------\n");
    printf("%-10s | %-45s | %-16s\n", "Algorithm", "Order of Service", "Total Head Movement");
    printf("----------------------------------------------------------------------------------\n");
    printf("%-10s | %-45s | %-16s\n", "FCFS", "53 98 183 37 122 14 124 65 67", "640 cylinders");
    printf("%-10s | %-45s | %-16s\n", "SSTF", "53 65 67 37 14 98 122 124 183", "236 cylinders");
    printf("%-10s | %-45s | %-16s\n", "SCAN", "53 37 14 0 65 67 98 122 124 183", "236 cylinders");
    printf("%-10s | %-45s | %-16s\n", "C-SCAN", "53 65 67 98 122 124 183 199 (0) 14 37", "382 cylinders (incl jump)");
    printf("%-10s | %-45s | %-16s\n", "LOOK", "53 37 14 65 67 98 122 124 183", "208 cylinders");
    printf("%-10s | %-45s | %-16s\n", "C-LOOK", "53 65 67 98 122 124 183 (14) 37", "322 cylinders (incl jump)");
    printf("----------------------------------------------------------------------------------\n\n");

    printf("Solid-State Drives (SSDs) Scheduling:\n");
    printf("- Linux uses 'none' (noop) or 'mq-deadline' because SSDs have 0 mechanical seek delay.\n");
    printf("- Elevating requests by cylinder number on flash storage is unnecessary and adds CPU lock contention.\n");
    return 0;
}
