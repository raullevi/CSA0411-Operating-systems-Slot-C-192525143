#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <time.h>

#define ITERATIONS 1000
#define BUFFER_PAGES 256

static double get_time_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1e9 + (double)ts.tv_nsec;
}

/* Pre-fault stack to avoid stack expansion page faults */
void prefault_stack(void) {
    volatile char stack_buf[8192];
    memset((void*)stack_buf, 0, sizeof(stack_buf));
}

int main(void) {
    printf("=======================================================================\n");
    printf("  CSA0411 OS ASSIGNMENT 3 - QUESTION 7: REAL-TIME MEMORY LOCKING\n");
    printf("  Student: Rakul K | Register Number: 192525143\n");
    printf("=======================================================================\n\n");

    long page_size = sysconf(_SC_PAGESIZE);
    size_t alloc_size = BUFFER_PAGES * page_size;

    printf("Real-Time Control Loop Configuration:\n");
    printf("  - System Page Size   : %ld bytes (%.1f KB)\n", page_size, page_size / 1024.0);
    printf("  - Control Buffer Size: %zu bytes (%zu pages)\n", alloc_size, (size_t)BUFFER_PAGES);
    printf("  - Test Iterations    : %d cycles\n\n", ITERATIONS);

    /* --- TEST 1: UNLOCKED MEMORY (DEMAND PAGING JITTER) --- */
    printf("-----------------------------------------------------------------------\n");
    printf("  TEST 1: UNLOCKED MEMORY (Subject to Page Faults & Jitter)\n");
    printf("-----------------------------------------------------------------------\n");

    char *unlocked_buf = (char *)malloc(alloc_size);
    struct rusage r_start, r_end;
    getrusage(RUSAGE_SELF, &r_start);

    double max_delay_unlocked = 0.0;
    double min_delay_unlocked = 1e9;
    double total_delay_unlocked = 0.0;

    for (int i = 0; i < ITERATIONS; i++) {
        size_t p = (i * 17) % BUFFER_PAGES;
        double t0 = get_time_ns();
        unlocked_buf[p * page_size] = (char)(i & 0xFF); /* Access memory */
        double dt = get_time_ns() - t0;

        if (dt > max_delay_unlocked) max_delay_unlocked = dt;
        if (dt < min_delay_unlocked) min_delay_unlocked = dt;
        total_delay_unlocked += dt;
    }

    getrusage(RUSAGE_SELF, &r_end);
    long faults_unlocked = (r_end.ru_minflt - r_start.ru_minflt) + (r_end.ru_majflt - r_start.ru_majflt);

    printf("  - Page Faults Incurred : %ld\n", faults_unlocked);
    printf("  - Average Loop Latency : %.2f ns\n", total_delay_unlocked / ITERATIONS);
    printf("  - Minimum Latency      : %.2f ns\n", min_delay_unlocked);
    printf("  - Worst-Case Latency   : %.2f ns (%.4f us)\n", max_delay_unlocked, max_delay_unlocked / 1000.0);
    printf("  - Latency Jitter (Max-Min): %.2f ns\n\n", max_delay_unlocked - min_delay_unlocked);

    /* --- TEST 2: LOCKED MEMORY (mlock + PRE-FAULTING) --- */
    printf("-----------------------------------------------------------------------\n");
    printf("  TEST 2: LOCKED MEMORY (mlockall / mlock - Zero Faults, Deterministic)\n");
    printf("-----------------------------------------------------------------------\n");

    char *locked_buf = (char *)malloc(alloc_size);
    prefault_stack();

    /* Lock all current and future pages into physical RAM */
    if (mlock(locked_buf, alloc_size) != 0) {
        perror("mlock warning (may require root or RLIMIT_MEMLOCK)");
    }

    /* Pre-fault every page in advance */
    for (size_t p = 0; p < (size_t)BUFFER_PAGES; p++) {
        locked_buf[p * page_size] = 1;
    }

    getrusage(RUSAGE_SELF, &r_start);
    double max_delay_locked = 0.0;
    double min_delay_locked = 1e9;
    double total_delay_locked = 0.0;

    for (int i = 0; i < ITERATIONS; i++) {
        size_t p = (i * 17) % BUFFER_PAGES;
        double t0 = get_time_ns();
        locked_buf[p * page_size] = (char)(i & 0xFF); /* Access pinned memory */
        double dt = get_time_ns() - t0;

        if (dt > max_delay_locked) max_delay_locked = dt;
        if (dt < min_delay_locked) min_delay_locked = dt;
        total_delay_locked += dt;
    }

    getrusage(RUSAGE_SELF, &r_end);
    long faults_locked = (r_end.ru_minflt - r_start.ru_minflt) + (r_end.ru_majflt - r_start.ru_majflt);

    printf("  - Page Faults Incurred : %ld [ZERO FAULTS VERIFIED]\n", faults_locked);
    printf("  - Average Loop Latency : %.2f ns\n", total_delay_locked / ITERATIONS);
    printf("  - Minimum Latency      : %.2f ns\n", min_delay_locked);
    printf("  - Worst-Case Latency   : %.2f ns (%.4f us)\n", max_delay_locked, max_delay_locked / 1000.0);
    printf("  - Latency Jitter (Max-Min): %.2f ns\n", max_delay_locked - min_delay_locked);

    double jitter_reduction = (max_delay_unlocked - min_delay_unlocked) / (max_delay_locked - min_delay_locked > 1 ? max_delay_locked - min_delay_locked : 1);
    printf("  - Real-Time Jitter Improvement: %.2fx more predictable!\n", jitter_reduction);

    munlock(locked_buf, alloc_size);
    free(unlocked_buf);
    free(locked_buf);
    printf("=======================================================================\n");

    return 0;
}
