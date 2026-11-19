#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <setjmp.h>
#include <stdint.h>

#define NUM_SEGMENTS 5
#define POOL_SIZE (1024 * 1024) /* 1 MB physical memory pool for fragmentation sim */

typedef struct {
    int seg_id;
    const char *name;
    unsigned int base;
    unsigned int limit;
    int read;
    int write;
    int execute;
} SegmentDescriptor;

/* Segment Table for Student Program */
static SegmentDescriptor seg_table[NUM_SEGMENTS] = {
    {0, "Code (Text)",          1400, 1000, 1, 0, 1},
    {1, "Data (Globals/BSS)",   6300,  400, 1, 1, 0},
    {2, "Stack",                4300,  500, 1, 1, 0},
    {3, "Shared Library (LibC)",3200, 1500, 1, 0, 1},
    {4, "Heap (Dynamic)",       8500,  600, 1, 1, 0}
};

/* 1. Translate 8 addresses */
void translate_8_addresses(void) {
    printf("=======================================================================\n");
    printf("  PART 1: SEGMENT ADDRESS TRANSLATION (8 VERIFICATION ADDRESSES)\n");
    printf("=======================================================================\n");
    printf("%-6s %-25s %-10s %-10s %-12s\n", "Seg#", "Segment Name", "Base", "Limit", "Perms");
    printf("-----------------------------------------------------------------------\n");
    for (int i = 0; i < NUM_SEGMENTS; i++) {
        char perms[4] = {seg_table[i].read ? 'R' : '-',
                         seg_table[i].write ? 'W' : '-',
                         seg_table[i].execute ? 'X' : '-', '\0'};
        printf("%-6d %-25s %-10u %-10u %-12s\n",
               seg_table[i].seg_id, seg_table[i].name,
               seg_table[i].base, seg_table[i].limit, perms);
    }
    printf("-----------------------------------------------------------------------\n\n");

    struct {
        int seg;
        unsigned int offset;
        const char *purpose;
    } test_addrs[8] = {
        {0,   50, "Instruction fetch from Code"},
        {0, 1050, "Execution buffer overrun in Code"},
        {1,  200, "Read global counter in Data"},
        {1,  400, "Array bounds violation in Data (offset == limit)"},
        {2,  150, "Stack push activation record"},
        {3,  720, "Call to shared compiler library"},
        {4,  300, "Malloc block read from Heap"},
        {5,   50, "Access non-existent Segment 5"}
    };

    printf("%-4s %-10s %-35s %-14s %-25s\n",
           "#", "Logical", "Access Description", "Status", "Physical Address / Trap");
    printf("---------------------------------------------------------------------------------------------\n");

    for (int i = 0; i < 8; i++) {
        int s = test_addrs[i].seg;
        unsigned int off = test_addrs[i].offset;

        printf("[%d]  (%d, %-4u)   %-35s ", i + 1, s, off, test_addrs[i].purpose);

        if (s < 0 || s >= NUM_SEGMENTS) {
            printf("%-14s TRAP: Invalid Segment Selector\n", "REJECTED");
        } else if (off >= seg_table[s].limit) {
            printf("%-14s TRAP: Offset (%u) >= Limit (%u) [SEGV]\n",
                   "REJECTED", off, seg_table[s].limit);
        } else {
            unsigned int phys = seg_table[s].base + off;
            printf("%-14s Valid: Base %u + Offset %u = %u\n",
                   "ACCEPTED", seg_table[s].base, off, phys);
        }
    }
    printf("---------------------------------------------------------------------------------------------\n\n");
}

/* 2. Trigger intentional hardware SIGSEGV and inspect signal info */
static jmp_buf segv_jmp;
static void *fault_addr = NULL;

static void handler_sigsegv(int sig, siginfo_t *info, void *ucontext) {
    (void)sig;
    (void)ucontext;
    fault_addr = info->si_addr;
    longjmp(segv_jmp, 1);
}

void trigger_segmentation_fault(void) {
    printf("=======================================================================\n");
    printf("  PART 2: TRIGGER HARDWARE SEGMENTATION FAULT (SIGSEGV) & OS ACTION\n");
    printf("=======================================================================\n");

    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sa.sa_sigaction = handler_sigsegv;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGSEGV, &sa, NULL);

    printf("Attempting illegal write to read-only memory address (NULL pointer dereference)...\n");

    if (sigsetjmp(segv_jmp, 1) == 0) {
        volatile int *bad_ptr = (volatile int *)0x0;
        *bad_ptr = 0xDEADBEEF; /* Hardware Fault! */
    } else {
        printf("[SUCCESSFUL TRAP] Hardware Memory Management Unit (MMU) triggered exception!\n");
        printf("  - Faulting Target Address : %p\n", fault_addr);
        printf("  - OS Kernel Action:\n");
        printf("    1. CPU detects segment/page protection violation.\n");
        printf("    2. CPU switches from User Mode (Ring 3) to Kernel Mode (Ring 0).\n");
        printf("    3. Kernel trap handler constructs siginfo_t and issues SIGSEGV.\n");
        printf("    4. If no signal handler: Kernel terminates process with Core Dump.\n");
        printf("    5. If handled: Execution transfers safely to registered handler.\n");
    }
    printf("\n");
}

/* 3. Simulate External Fragmentation: 20 Random Segment Allocations/Deallocations */
typedef struct MemBlock {
    unsigned int start;
    unsigned int size;
    int is_free;
    struct MemBlock *next;
} MemBlock;

void simulate_segment_fragmentation(void) {
    printf("=======================================================================\n");
    printf("  PART 3: EXTERNAL FRAGMENTATION SIMULATION (20 DYNAMIC SEGMENTS)\n");
    printf("=======================================================================\n");

    MemBlock *head = (MemBlock *)malloc(sizeof(MemBlock));
    head->start = 0;
    head->size = POOL_SIZE;
    head->is_free = 1;
    head->next = NULL;

    srand(192525143);
    unsigned int segment_sizes[20];
    MemBlock* allocated_ptrs[20];

    printf("Simulating dynamic segment lifecycle (Allocation & Freeing)...\n");

    /* Phase 1: Allocate 20 segments of variable sizes (10 KB to 90 KB) */
    for (int i = 0; i < 20; i++) {
        segment_sizes[i] = (unsigned int)((rand() % 80 + 10) * 1024);
        allocated_ptrs[i] = NULL;

        MemBlock *curr = head;
        while (curr) {
            if (curr->is_free && curr->size >= segment_sizes[i]) {
                if (curr->size > segment_sizes[i]) {
                    MemBlock *remainder = (MemBlock *)malloc(sizeof(MemBlock));
                    remainder->start = curr->start + segment_sizes[i];
                    remainder->size = curr->size - segment_sizes[i];
                    remainder->is_free = 1;
                    remainder->next = curr->next;
                    curr->next = remainder;
                }
                curr->size = segment_sizes[i];
                curr->is_free = 0;
                allocated_ptrs[i] = curr;
                break;
            }
            curr = curr->next;
        }
    }

    /* Phase 2: Free alternating segments */
    for (int i = 0; i < 20; i += 2) {
        if (allocated_ptrs[i]) {
            allocated_ptrs[i]->is_free = 1;
            allocated_ptrs[i] = NULL;
        }
    }

    /* Measure Fragmentation */
    unsigned int total_free_bytes = 0;
    unsigned int largest_contiguous_hole = 0;
    int free_hole_count = 0;

    MemBlock *curr = head;
    while (curr) {
        if (curr->is_free) {
            total_free_bytes += curr->size;
            free_hole_count++;
            if (curr->size > largest_contiguous_hole) {
                largest_contiguous_hole = curr->size;
            }
        }
        curr = curr->next;
    }

    unsigned int large_job_request = 150 * 1024;
    int can_allocate = (largest_contiguous_hole >= large_job_request);

    printf("Fragmentation Metrics After 20 Segment Allocation/Deallocation Cycles:\n");
    printf("  - Total Physical Pool Size        : %u KB (1.0 MB)\n", POOL_SIZE / 1024);
    printf("  - Total Free Memory Available     : %u KB (%.1f%% free)\n",
           total_free_bytes / 1024, (total_free_bytes * 100.0) / POOL_SIZE);
    printf("  - Number of Disjoint Free Holes   : %d holes (Checkerboarding)\n", free_hole_count);
    printf("  - Largest Contiguous Free Block   : %u KB\n", largest_contiguous_hole / 1024);
    printf("  - Incoming Large Student Job Req  : %u KB\n", large_job_request / 1024);
    printf("  - Allocation Result               : %s!\n",
           can_allocate ? "SUCCESS" : "FAILED (EXTERNAL FRAGMENTATION REJECTION)");

    double external_frag_pct = (1.0 - ((double)largest_contiguous_hole / (double)total_free_bytes)) * 100.0;
    printf("  - Calculated External Fragmentation: %.2f%%\n", external_frag_pct);

    curr = head;
    while (curr) {
        MemBlock *temp = curr;
        curr = curr->next;
        free(temp);
    }
    printf("\n");
}

/* 4. Display segments of running program */
void show_current_process_segments(void) {
    printf("=======================================================================\n");
    printf("  PART 4: RUNNING PROCESS MEMORY SEGMENT INSPECTION\n");
    printf("=======================================================================\n");
    printf("Process PID: %d\n", getpid());
    printf("Logical Memory Segments:\n");
    printf("  - Code / Text Segment     (&translate_8_addresses): %p\n", (void*)(uintptr_t)translate_8_addresses);
    printf("  - Initialized Data Segment (seg_table)             : %p\n", (void*)seg_table);
    int stack_var = 100;
    printf("  - Stack Segment            (&stack_var)            : %p\n", (void*)&stack_var);
    void *heap_var = malloc(1024);
    printf("  - Heap Segment             (malloc buffer)         : %p\n", heap_var);
    free(heap_var);
    printf("=======================================================================\n");
}

int main(void) {
    printf("=======================================================================\n");
    printf("  CSA0411 OS ASSIGNMENT 3 - QUESTION 3 SEGMENTATION\n");
    printf("  Student: Rakul K | Register Number: 192525143\n");
    printf("=======================================================================\n\n");

    translate_8_addresses();
    trigger_segmentation_fault();
    simulate_segment_fragmentation();
    show_current_process_segments();

    return 0;
}
