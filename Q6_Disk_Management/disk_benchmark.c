#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/time.h>

#define FILE_SIZE_MB 32
#define FILE_BYTES ((size_t)FILE_SIZE_MB * 1024 * 1024)
#define BLOCK_SIZE 4096

static double get_time_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

int main(void) {
    printf("=======================================================================\n");
    printf("  CSA0411 OS ASSIGNMENT 3 - QUESTION 6 DISK BENCHMARK\n");
    printf("  Student: Rakul K | Register Number: 192525143\n");
    printf("=======================================================================\n\n");

    const char *test_file = "test_io_benchmark.tmp";
    printf("Creating %d MB test file (%s)...\n", FILE_SIZE_MB, test_file);

    int fd = open(test_file, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0) {
        perror("open for write failed");
        return 1;
    }

    char *buf = (char *)malloc(BLOCK_SIZE);
    memset(buf, 0x55, BLOCK_SIZE);

    size_t num_blocks = FILE_BYTES / BLOCK_SIZE;
    double t_write_start = get_time_sec();
    for (size_t i = 0; i < num_blocks; i++) {
        if (write(fd, buf, BLOCK_SIZE) != BLOCK_SIZE) {
            perror("write error");
            close(fd);
            return 1;
        }
    }
    fsync(fd);
    double t_write = get_time_sec() - t_write_start;
    close(fd);

    printf("Sequential Write: %.2f MB/s (Time: %.4f s)\n",
           (double)FILE_SIZE_MB / t_write, t_write);

    /* 1. Sequential Read Benchmark */
    fd = open(test_file, O_RDONLY);
    if (fd < 0) {
        perror("open for read failed");
        return 1;
    }

    double t_seq_start = get_time_sec();
    for (size_t i = 0; i < num_blocks; i++) {
        if (read(fd, buf, BLOCK_SIZE) != BLOCK_SIZE) {
            perror("seq read error");
            break;
        }
    }
    double t_seq = get_time_sec() - t_seq_start;
    printf("Sequential Read : %.2f MB/s (Time: %.4f s)\n",
           (double)FILE_SIZE_MB / t_seq, t_seq);

    /* 2. Random Read Benchmark (Simulating Hospital Records Patient Lookup) */
    size_t random_samples = 4000;
    double t_rand_start = get_time_sec();
    for (size_t i = 0; i < random_samples; i++) {
        off_t offset = (off_t)((rand() % num_blocks) * BLOCK_SIZE);
        lseek(fd, offset, SEEK_SET);
        if (read(fd, buf, BLOCK_SIZE) != BLOCK_SIZE) {
            perror("rand read error");
            break;
        }
    }
    double t_rand = get_time_sec() - t_rand_start;
    double rand_mb = (double)(random_samples * BLOCK_SIZE) / (1024.0 * 1024.0);
    double avg_latency_ms = (t_rand / (double)random_samples) * 1000.0;

    printf("Random Read     : %.2f MB/s (Average I/O Latency: %.4f ms per 4KB record)\n",
           rand_mb / t_rand, avg_latency_ms);

    close(fd);
    unlink(test_file);
    free(buf);

    printf("\nAnalysis: Flash SSD NVMe storage delivers sub-millisecond random I/O latency\n");
    printf("whereas mechanical spinning HDDs suffer 8-15 ms seek latency per random read.\n");
    return 0;
}
