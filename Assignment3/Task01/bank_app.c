#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include "libencrypt.h"

int main(int argc, char **argv) {
    printf("=================================================================\n");
    printf("  BANK BRANCH TRANSACTION TERMINAL - CSA04 OS Assignment 3 (CO3)\n");
    printf("  Student: Rakul K | Register Number: 192525143\n");
    printf("=================================================================\n");
    printf("PID: %d\n", getpid());
    printf("Active Security Module: %s\n", get_encryption_version());
    printf("Security Patch Status : %s\n", is_security_patch_active() ? "SECURE (PATCHED)" : "CRITICAL RISK (UNPATCHED)");

    const char *sensitive_tx = "TX#99281: SENDER=ACC_4412 AMOUNT=$1,500,000 RECIPIENT=ACC_8801";
    char ciphertext[128] = {0};
    char decrypted[128] = {0};
    size_t len = strlen(sensitive_tx);

    encrypt_payload(sensitive_tx, ciphertext, len);
    printf("Plaintext Transaction  : \"%s\"\n", sensitive_tx);
    printf("Encrypted Cipher Payload (Hex): ");
    for (size_t i = 0; i < len; i++) {
        printf("%02X ", (unsigned char)ciphertext[i]);
    }
    printf("\n");

    decrypt_payload(ciphertext, decrypted, len);
    printf("Decrypted Transaction  : \"%s\"\n", decrypted);

    printf("\n=== Process Memory Map Inspection (/proc/self/maps) ===\n");
    FILE *f = fopen("/proc/self/maps", "r");
    if (f) {
        char line[256];
        int count = 0;
        while (fgets(line, sizeof(line), f) && count < 25) {
            printf("%s", line);
            count++;
        }
        fclose(f);
    } else {
        printf("[Note: /proc/self/maps is Linux-specific (or in Linux container/procfs).\n");
        printf("       Inspecting runtime symbol and segment addresses directly:]\n");
        printf("  - Main function address (&main)             : %p\n", (void*)(uintptr_t)main);
        printf("  - Library function (&get_encryption_version): %p\n", (void*)(uintptr_t)get_encryption_version);
        printf("  - Library function (&encrypt_payload)       : %p\n", (void*)(uintptr_t)encrypt_payload);
        printf("  - C library function (&printf)              : %p\n", (void*)(uintptr_t)printf);
        void *heap_alloc = malloc(1024);
        printf("  - Heap allocated memory buffer              : %p\n", heap_alloc);
        int stack_var = 42;
        printf("  - Stack local variable (&stack_var)         : %p\n", (void*)&stack_var);
        free(heap_alloc);
    }

    /* If user passed pause flag, wait for multi-instance inspection */
    if (argc > 1 && strcmp(argv[1], "--pause") == 0) {
        printf("\nProcess is pausing for 10 seconds to allow multi-instance inspection...\n");
        fflush(stdout);
        sleep(10);
    }

    printf("\nTransaction completed successfully.\n");
    return 0;
}
