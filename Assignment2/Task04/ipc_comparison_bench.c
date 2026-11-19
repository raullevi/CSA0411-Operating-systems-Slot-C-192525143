/**
 * Task 04: IPC Benchmark - Pipe vs Shared Memory (1 MB, 10 MB, 100 MB)
 * Course: CSA0411 / CSA04 - Operating Systems (Slot C)
 * Student: Rakul K | Register Number: 192525143
 */

#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <time.h>
#include <pthread.h>
#include <fcntl.h>

#ifndef MAP_ANONYMOUS
#ifdef MAP_ANON
#define MAP_ANONYMOUS MAP_ANON
#else
#define MAP_ANONYMOUS 0x1000
#endif
#endif

#define CHUNK_SIZE (64 * 1024) /* 64 KB write chunks */

static double get_time_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/* Benchmark Pipe IPC */
double bench_pipe(size_t total_bytes) {
    int fd[2];
    if (pipe(fd) == -1) { perror("pipe"); return -1; }

    char *chunk = malloc(CHUNK_SIZE);
    if (!chunk) return -1;
    memset(chunk, 'W', CHUNK_SIZE);

    double start = get_time_sec();
    pid_t pid = fork();
    if (pid == 0) {
        close(fd[1]);
        char *recv_buf = malloc(CHUNK_SIZE);
        size_t received = 0;
        ssize_t n;
        while ((n = read(fd[0], recv_buf, CHUNK_SIZE)) > 0) {
            received += n;
            if (received >= total_bytes) break;
        }
        free(recv_buf);
        close(fd[0]);
        _exit(0);
    }

    close(fd[0]);
    size_t sent = 0;
    while (sent < total_bytes) {
        size_t to_write = (total_bytes - sent < CHUNK_SIZE) ? (total_bytes - sent) : CHUNK_SIZE;
        ssize_t w = write(fd[1], chunk, to_write);
        if (w <= 0) break;
        sent += w;
    }
    close(fd[1]);
    waitpid(pid, NULL, 0);
    double elapsed = get_time_sec() - start;

    free(chunk);
    return elapsed;
}

/* Benchmark Shared Memory IPC with Process-Shared Mutex & Cond */
typedef struct {
    pthread_mutex_t mutex;
    pthread_cond_t cond_read;
    pthread_cond_t cond_write;
    size_t bytes_ready;
    int done;
    char buffer[CHUNK_SIZE];
} ShmControl;

double bench_shm(size_t total_bytes) {
    ShmControl *shm = mmap(NULL, sizeof(ShmControl),
                           PROT_READ | PROT_WRITE,
                           MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (shm == MAP_FAILED) { perror("mmap"); return -1; }

    pthread_mutexattr_t mattr;
    pthread_mutexattr_init(&mattr);
    pthread_mutexattr_setpshared(&mattr, PTHREAD_PROCESS_SHARED);
    pthread_mutex_init(&shm->mutex, &mattr);
    pthread_mutexattr_destroy(&mattr);

    pthread_condattr_t cattr;
    pthread_condattr_init(&cattr);
    pthread_condattr_setpshared(&cattr, PTHREAD_PROCESS_SHARED);
    pthread_cond_init(&shm->cond_read, &cattr);
    pthread_cond_init(&shm->cond_write, &cattr);
    pthread_condattr_destroy(&cattr);

    shm->bytes_ready = 0;
    shm->done = 0;

    char *chunk = malloc(CHUNK_SIZE);
    if (!chunk) return -1;
    memset(chunk, 'S', CHUNK_SIZE);

    double start = get_time_sec();
    pid_t pid = fork();
    if (pid == 0) {
        size_t received = 0;
        char *recv_buf = malloc(CHUNK_SIZE);
        while (received < total_bytes) {
            pthread_mutex_lock(&shm->mutex);
            while (shm->bytes_ready == 0 && !shm->done) {
                pthread_cond_wait(&shm->cond_read, &shm->mutex);
            }
            if (shm->bytes_ready > 0) {
                size_t b = shm->bytes_ready;
                memcpy(recv_buf, shm->buffer, b);
                received += b;
                shm->bytes_ready = 0;
                pthread_cond_signal(&shm->cond_write);
            }
            pthread_mutex_unlock(&shm->mutex);
        }
        free(recv_buf);
        _exit(0);
    }

    size_t sent = 0;
    while (sent < total_bytes) {
        size_t to_write = (total_bytes - sent < CHUNK_SIZE) ? (total_bytes - sent) : CHUNK_SIZE;
        pthread_mutex_lock(&shm->mutex);
        while (shm->bytes_ready > 0) {
            pthread_cond_wait(&shm->cond_write, &shm->mutex);
        }
        memcpy(shm->buffer, chunk, to_write);
        shm->bytes_ready = to_write;
        sent += to_write;
        if (sent >= total_bytes) shm->done = 1;
        pthread_cond_signal(&shm->cond_read);
        pthread_mutex_unlock(&shm->mutex);
    }

    waitpid(pid, NULL, 0);
    double elapsed = get_time_sec() - start;

    pthread_mutex_destroy(&shm->mutex);
    pthread_cond_destroy(&shm->cond_read);
    pthread_cond_destroy(&shm->cond_write);
    munmap(shm, sizeof(ShmControl));
    free(chunk);
    return elapsed;
}

int main(void) {
    printf("======================================================================\n");
    printf("  CSA0411 OPERATING SYSTEMS - ASSIGNMENT 2 (CO2)\n");
    printf("  Task 04: IPC Benchmark - Pipe vs Shared Memory (1MB, 10MB, 100MB)\n");
    printf("  Student: Rakul K (Reg No: 192525143)\n");
    printf("======================================================================\n\n");

    size_t sizes[] = {1 * 1024 * 1024, 10 * 1024 * 1024, 100 * 1024 * 1024};
    const char *labels[] = {"1 MB", "10 MB", "100 MB"};

    printf("%-10s | %-16s | %-16s | %-16s | %-16s\n",
           "Data Size", "Pipe Time (s)", "Pipe Rate (MB/s)", "SHM Time (s)", "SHM Rate (MB/s)");
    printf("----------------------------------------------------------------------------------\n");

    for (int i = 0; i < 3; i++) {
        size_t bytes = sizes[i];
        double mb = (double)bytes / (1024.0 * 1024.0);

        double t_pipe = bench_pipe(bytes);
        double rate_pipe = (t_pipe > 0.0) ? (mb / t_pipe) : 0.0;

        double t_shm = bench_shm(bytes);
        double rate_shm = (t_shm > 0.0) ? (mb / t_shm) : 0.0;

        printf("%-10s | %14.4f s | %11.2f MB/s | %13.4f s | %10.2f MB/s\n",
               labels[i], t_pipe, rate_pipe, t_shm, rate_shm);
    }
    printf("----------------------------------------------------------------------------------\n\n");
    printf("Key Findings:\n");
    printf("1. Shared memory avoids kernel buffer double-copying, achieving significantly higher throughput.\n");
    printf("2. Pipes require user->kernel and kernel->user copies, plus context switches on buffer full/empty.\n");
    printf("3. For streaming weather telemetry (< few KB/s), pipes provide simple implicit synchronization (EOF on close).\n");
    return 0;
}
