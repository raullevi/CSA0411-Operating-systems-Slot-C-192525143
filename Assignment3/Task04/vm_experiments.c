#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>

#define BUFFER_MB 64
#define BUFFER_SIZE ((size_t)BUFFER_MB * 1024 * 1024)
#define COW_MB 32
#define COW_SIZE ((size_t)COW_MB * 1024 * 1024)

static double get_time_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

/* 1. Sequential vs Random Locality Benchmark */
void run_locality_benchmark(void) {
    printf("==================================================================\n");
    printf("  PART 1: MEMORY ACCESS LOCALITY BENCHMARK (SEQUENTIAL VS RANDOM)\n");
    printf("==================================================================\n");
    printf("Allocating %d MB test buffer...\n", BUFFER_MB);

    char *buf = (char *)malloc(BUFFER_SIZE);
    if (!buf) {
        perror("malloc failed");
        return;
    }

    struct rusage r_start, r_seq, r_rand;
    long page_size = sysconf(_SC_PAGESIZE);
    size_t num_pages = BUFFER_SIZE / page_size;

    /* A. Sequential Access (Strong Locality) */
    getrusage(RUSAGE_SELF, &r_start);
    double t0 = get_time_sec();

    for (size_t p = 0; p < num_pages; p++) {
        buf[p * page_size] = (char)(p & 0xFF);
    }

    double t_seq = get_time_sec() - t0;
    getrusage(RUSAGE_SELF, &r_seq);

    long minflt_seq = r_seq.ru_minflt - r_start.ru_minflt;
    long majflt_seq = r_seq.ru_majflt - r_start.ru_majflt;

    printf("\n[1] Sequential Access (Spatial & Temporal Locality):\n");
    printf("    - Execution Time : %.4f seconds\n", t_seq);
    printf("    - Minor Faults   : %ld page reclaims\n", minflt_seq);
    printf("    - Major Faults   : %ld disk I/O faults\n", majflt_seq);

    /* B. Random Stride Access (Poor Locality) */
    double t1 = get_time_sec();
    size_t stride = 9973; /* Prime stride across pages */
    for (size_t i = 0; i < num_pages * 2; i++) {
        size_t p = (i * stride) % num_pages;
        buf[p * page_size] += 1;
    }

    double t_rand = get_time_sec() - t1;
    getrusage(RUSAGE_SELF, &r_rand);

    long minflt_rand = r_rand.ru_minflt - r_seq.ru_minflt;
    long majflt_rand = r_rand.ru_majflt - r_seq.ru_majflt;

    printf("\n[2] Random Stride Access (Scattered Access):\n");
    printf("    - Execution Time : %.4f seconds\n", t_rand);
    printf("    - Minor Faults   : %ld page reclaims\n", minflt_rand);
    printf("    - Major Faults   : %ld disk I/O faults\n", majflt_rand);
    printf("    - Performance Ratio (Random vs Seq): %.2fx slower\n", t_rand / (t_seq > 0.0001 ? t_seq : 0.0001));

    free(buf);
    printf("\n");
}

/* 2. Copy-on-Write (COW) Fork Benchmark */
void run_cow_benchmark(void) {
    printf("==================================================================\n");
    printf("  PART 2: COPY-ON-WRITE (COW) DEMONSTRATION WITH fork()\n");
    printf("==================================================================\n");
    printf("Allocating %d MB memory block in Parent...\n", COW_MB);

    char *shared_block = (char *)malloc(COW_SIZE);
    if (!shared_block) return;
    memset(shared_block, 0xAA, COW_SIZE); /* Touch all pages in Parent */

    struct rusage parent_usage;
    getrusage(RUSAGE_SELF, &parent_usage);
    printf("Parent RSS before fork(): %ld KB\n", parent_usage.ru_maxrss / 1024);

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        return;
    }

    if (pid == 0) {
        /* Child Process */
        struct rusage child_before, child_after;
        getrusage(RUSAGE_SELF, &child_before);
        printf("  [Child Immediately After fork()] RSS: %ld KB (Zero duplicate copies!)\n",
               child_before.ru_maxrss / 1024);

        /* Write to 25% of pages to trigger Copy-on-Write faults */
        long page_size = sysconf(_SC_PAGESIZE);
        size_t pages_to_write = (COW_SIZE / page_size) / 4;
        for (size_t i = 0; i < pages_to_write; i++) {
            shared_block[i * page_size] = 0x55; /* Triggers hardware COW fault */
        }

        getrusage(RUSAGE_SELF, &child_after);
        long cow_faults = child_after.ru_minflt - child_before.ru_minflt;
        printf("  [Child After Writing 25%% Pages] COW Minor Faults Triggered: %ld\n", cow_faults);
        printf("  [Child Final RSS]                : %ld KB\n", child_after.ru_maxrss / 1024);

        free(shared_block);
        exit(0);
    } else {
        /* Parent Process */
        wait(NULL);
        free(shared_block);
        printf("[Parent] Child finished. COW allows instant fork() without copying RAM.\n\n");
    }
}

/* 3. Medical Imaging Reference String Simulation: Page Faults vs Frame Count */
void run_page_fault_curve(void) {
    printf("==================================================================\n");
    printf("  PART 3: MEDICAL IMAGING REFERENCE STRING - FAULTS VS FRAMES\n");
    printf("==================================================================\n");

    /* Simulated medical scan slice reference string (repeated passes over 10 slices) */
    int ref_string[] = {
        1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5,
        6, 7, 8, 2, 3, 4, 7, 8, 9, 10, 1, 2,
        3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4
    };
    int len = sizeof(ref_string) / sizeof(ref_string[0]);

    printf("Simulating 36-access medical scan string over frame allocations 1 to 10...\n");
    printf("%-8s %-15s %-18s %-15s\n", "Frames", "Page Faults", "Fault Rate (%)", "Hit Rate (%)");
    printf("-------------------------------------------------------------\n");

    FILE *f_csv = fopen("page_fault_curve.csv", "w");
    if (f_csv) fprintf(f_csv, "frames,faults,fault_rate\n");

    for (int frames = 1; frames <= 10; frames++) {
        int memory[16];
        int used = 0;
        int faults = 0;

        for (int i = 0; i < len; i++) {
            int page = ref_string[i];
            int hit = 0;
            for (int k = 0; k < used; k++) {
                if (memory[k] == page) {
                    hit = 1;
                    break;
                }
            }

            if (!hit) {
                faults++;
                if (used < frames) {
                    memory[used++] = page;
                } else {
                    /* FIFO replacement for reference */
                    for (int k = 0; k < frames - 1; k++) {
                        memory[k] = memory[k + 1];
                    }
                    memory[frames - 1] = page;
                }
            }
        }

        double fault_rate = ((double)faults / (double)len) * 100.0;
        double hit_rate = 100.0 - fault_rate;

        printf("%-8d %-15d %-18.2f %-15.2f\n", frames, faults, fault_rate, hit_rate);
        if (f_csv) fprintf(f_csv, "%d,%d,%.2f\n", frames, faults, fault_rate);
    }

    if (f_csv) fclose(f_csv);
    printf("-------------------------------------------------------------\n");
    printf("Saved data to 'page_fault_curve.csv' for plotting.\n\n");
}

/* 4. Effective Access Time (EAT) Math Calculations */
void print_eat_evaluations(void) {
    printf("==================================================================\n");
    printf("  PART 4: EFFECTIVE ACCESS TIME (EAT) EVALUATION MATRIX\n");
    printf("==================================================================\n");
    printf("Parameters: Memory Access t_mem = 100 ns, Page Fault Service t_fault = 8 ms = 8,000,000 ns\n");
    printf("Formula   : EAT = (1 - p) * 100 + p * 8,000,000 = 100 + p * 7,999,900 ns\n\n");

    double probs[] = {1.0 / 1000.0, 1.0 / 100000.0, 1.0 / 1000000.0};
    const char *p_strs[] = {"1 in 1,000 (0.1%)", "1 in 100,000 (0.001%)", "1 in 1,000,000 (0.0001%)"};

    printf("%-24s %-16s %-16s %-14s\n", "Page Fault Rate (p)", "EAT (ns)", "EAT (microseconds)", "Slowdown");
    printf("-----------------------------------------------------------------------\n");
    for (int i = 0; i < 3; i++) {
        double p = probs[i];
        double eat = 100.0 + p * 7999900.0;
        double slowdown = eat / 100.0;
        printf("%-24s %14.2f ns %14.4f us %12.2fx\n",
               p_strs[i], eat, eat / 1000.0, slowdown);
    }
    printf("-----------------------------------------------------------------------\n\n");

    /* Calculate max p for 10% slowdown */
    double p_max = 10.0 / 7999900.0;
    printf("Maximum Acceptable Page-Fault Rate for <= 10%% Slowdown:\n");
    printf("  Target EAT <= 1.10 * 100 ns = 110 ns\n");
    printf("  p_max = 10 / 7,999,900 = %.8f (approx 1 in %ld accesses)\n",
           p_max, (long)(1.0 / p_max));
    printf("==================================================================\n");
}

int main(void) {
    printf("==================================================================\n");
    printf("  CSA0411 OS ASSIGNMENT 3 - QUESTION 4 VIRTUAL MEMORY\n");
    printf("  Student: Rakul K | Register Number: 192525143\n");
    printf("==================================================================\n\n");

    print_eat_evaluations();
    run_locality_benchmark();
    run_cow_benchmark();
    run_page_fault_curve();

    return 0;
}
