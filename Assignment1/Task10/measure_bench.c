/**
 * Task 10: Measure and Compare - 1,000 Processes vs 1,000 Threads Benchmark
 * Course: CSA0411 / CSA04 - Operating Systems (Slot C)
 * Student: Rakul K | Register Number: 192525143
 */

#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <pthread.h>
#include <time.h>

#define N 1000

static double get_time_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void *dummy_thread_func(void *arg) {
    (void)arg;
    return NULL;
}

double benchmark_processes(void) {
    double start = get_time_sec();
    for (int i = 0; i < N; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            _exit(0);
        } else if (pid > 0) {
            waitpid(pid, NULL, 0);
        } else {
            perror("fork failed");
            break;
        }
    }
    double elapsed = get_time_sec() - start;
    return elapsed;
}

double benchmark_threads(void) {
    pthread_t th[N];
    double start = get_time_sec();
    for (int i = 0; i < N; i++) {
        pthread_create(&th[i], NULL, dummy_thread_func, NULL);
    }
    for (int i = 0; i < N; i++) {
        pthread_join(th[i], NULL);
    }
    double elapsed = get_time_sec() - start;
    return elapsed;
}

int main(void) {
    printf("======================================================================\n");
    printf("  CSA0411 OPERATING SYSTEMS - ASSIGNMENT 1 (CO1)\n");
    printf("  Task 10: Process Creation vs Thread Creation Microbenchmark (N = %d)\n", N);
    printf("  Student: Rakul K (Reg No: 192525143)\n");
    printf("======================================================================\n\n");

    printf("Measuring sequential creation and teardown of %d OS Processes...\n", N);
    double t_proc = benchmark_processes();
    double avg_proc_us = (t_proc / N) * 1e6;

    printf("Measuring concurrent creation and joining of %d POSIX Threads...\n", N);
    double t_th = benchmark_threads();
    double avg_th_us = (t_th / N) * 1e6;

    printf("\n----------------------------------------------------------------------\n");
    printf("%-20s | %-16s | %-16s | %-12s\n", "Entity", "Total Time (s)", "Avg Cost / Unit", "Speedup");
    printf("----------------------------------------------------------------------\n");
    printf("%-20s | %14.4f s | %13.2f us | 1.00x (Baseline)\n", "1,000 Processes", t_proc, avg_proc_us);
    printf("%-20s | %14.4f s | %13.2f us | %5.2fx Faster\n", "1,000 Threads", t_th, avg_th_us, t_proc / t_th);
    printf("----------------------------------------------------------------------\n\n");

    printf("Evaluation:\n");
    printf("1. Thread creation is vastly faster because threads share address space and page tables.\n");
    printf("2. Process creation requires duplicating task structures, memory maps, and file descriptor tables.\n");
    return 0;
}
