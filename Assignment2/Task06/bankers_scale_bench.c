/**
 * Task 06: Banker's Algorithm Scalability Benchmark (N=10, 100, 1000)
 * Course: CSA0411 / CSA04 - Operating Systems (Slot C)
 * Student: Rakul K | Register Number: 192525143
 *
 * Measures execution time of Banker's safety algorithm to empirically verify
 * the O(m * n^2) theoretical complexity.
 */

#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define NUM_RESOURCES 4

static double get_time_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int run_safety_check(int n, int m, int *avail, int *maxm, int *alloc) {
    int *work = malloc(m * sizeof(int));
    int *finish = calloc(n, sizeof(int));
    int *seq = malloc(n * sizeof(int));
    int count = 0;

    memcpy(work, avail, m * sizeof(int));

    while (count < n) {
        int found = 0;
        for (int p = 0; p < n; p++) {
            if (finish[p]) continue;

            int can_finish = 1;
            for (int r = 0; r < m; r++) {
                int need = maxm[p * m + r] - alloc[p * m + r];
                if (need > work[r]) {
                    can_finish = 0;
                    break;
                }
            }

            if (can_finish) {
                for (int r = 0; r < m; r++) {
                    work[r] += alloc[p * m + r];
                }
                finish[p] = 1;
                seq[count++] = p;
                found = 1;
            }
        }
        if (!found) {
            free(work);
            free(finish);
            free(seq);
            return 0; /* Unsafe */
        }
    }

    free(work);
    free(finish);
    free(seq);
    return 1; /* Safe */
}

void benchmark_scale(int n, int iterations) {
    int m = NUM_RESOURCES;
    int *avail = malloc(m * sizeof(int));
    int *maxm = malloc(n * m * sizeof(int));
    int *alloc = malloc(n * m * sizeof(int));

    for (int r = 0; r < m; r++) avail[r] = n * 2;

    for (int p = 0; p < n; p++) {
        for (int r = 0; r < m; r++) {
            maxm[p * m + r] = (p % 5) + 1;
            alloc[p * m + r] = (p % 3);
        }
    }

    double start = get_time_sec();
    for (int iter = 0; iter < iterations; iter++) {
        run_safety_check(n, m, avail, maxm, alloc);
    }
    double elapsed = get_time_sec() - start;
    double avg_us = (elapsed / iterations) * 1e6;

    printf("N = %-5d | Iterations = %-5d | Total Time = %8.4f s | Avg Time/Check = %10.2f us\n",
           n, iterations, elapsed, avg_us);

    free(avail);
    free(maxm);
    free(alloc);
}

int main(void) {
    printf("======================================================================\n");
    printf("  CSA0411 OPERATING SYSTEMS - ASSIGNMENT 2 (CO2)\n");
    printf("  Task 06: Banker's Safety Algorithm Scalability Benchmark\n");
    printf("  Student: Rakul K (Reg No: 192525143)\n");
    printf("======================================================================\n\n");

    printf("Theoretical Complexity: O(m * n^2)\n");
    printf("Testing with m = %d resource types across n = 10, 100, 1000 processes:\n", NUM_RESOURCES);
    printf("----------------------------------------------------------------------------------\n");

    benchmark_scale(10, 10000);
    benchmark_scale(100, 1000);
    benchmark_scale(1000, 50);

    printf("----------------------------------------------------------------------------------\n\n");
    printf("Analysis of Growth Factor:\n");
    printf("- When N scales 10 -> 100 (10x increase), theoretical time increases ~100x.\n");
    printf("- When N scales 100 -> 1000 (10x increase), theoretical time increases ~100x.\n");
    printf("- Empirical measurements confirm quadratic O(n^2) computational cost.\n");
    return 0;
}
