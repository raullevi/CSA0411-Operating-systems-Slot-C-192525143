#include <stdio.h>

#define PAGES 8

/* Run address translation for a specific page size */
void run_translation(int page_size, const char *label) {
    /* Page table of a process: frame number, or -1 if the page is not in memory. */
    int page_table[PAGES] = {5, 2, -1, 7, 0, -1, 3, -1};
    unsigned logical[] = {0, 1500, 3100, 6200, 9000, 2049};
    int n = sizeof(logical) / sizeof(logical[0]);

    printf("===============================================================\n");
    printf("  Paging Translation Test: %s (PAGE_SIZE = %d, PAGES = %d)\n", label, page_size, PAGES);
    printf("===============================================================\n");
    printf("Page Table Mapping:\n");
    for (int p = 0; p < PAGES; p++) {
        if (page_table[p] >= 0) {
            printf("  Page %d -> Frame %d\n", p, page_table[p]);
        } else {
            printf("  Page %d -> [NOT IN MEMORY / INVALID]\n", p);
        }
    }
    printf("---------------------------------------------------------------\n");

    for (int i = 0; i < n; i++) {
        unsigned a = logical[i];
        
        // TODO 1: Split a into page number a / PAGE_SIZE and offset d = a % PAGE_SIZE.
        // If p is outside the table print "invalid address"; if the frame is -1 print "page fault";
        // otherwise print the physical address frame * PAGE_SIZE + d
        unsigned p = a / page_size;
        unsigned d = a % page_size;

        printf("%u -> page %u offset %u : ", a, p, d);

        if (p >= PAGES) {
            printf("invalid address\n");
        } else if (page_table[p] == -1) {
            printf("page fault\n");
        } else {
            unsigned frame = (unsigned)page_table[p];
            unsigned physical = frame * page_size + d;
            printf("physical %u\n", physical);
        }
    }
    printf("\n");
}

int main(void) {
    printf("CSA0411 OS Assignment 3 - Question 2: Complete the Code\n");
    printf("Student: Rakul K | Register Number: 192525143\n\n");

    /* Part 1: Default configuration with PAGE_SIZE = 1024 */
    run_translation(1024, "Part 1 (Prompt Default)");

    /* Part 2: Recalculated configuration with PAGE_SIZE = 2048 */
    run_translation(2048, "Part 2 (Recalculated with PAGE_SIZE = 2048)");

    return 0;
}
