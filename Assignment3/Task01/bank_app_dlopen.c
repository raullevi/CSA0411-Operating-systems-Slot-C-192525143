#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dlfcn.h>
#include <unistd.h>

typedef const char* (*fn_get_version)(void);
typedef void (*fn_encrypt)(const char*, char*, size_t);
typedef void (*fn_decrypt)(const char*, char*, size_t);
typedef int (*fn_is_patched)(void);

int main(int argc, char **argv) {
    const char *lib_path = (argc > 1) ? argv[1] : "./libencrypt.so";

    printf("=================================================================\n");
    printf("  DYNAMIC RUNTIME LOADER (dlopen / dlsym) - BANK SYSTEM\n");
    printf("  Target Shared Library: %s\n", lib_path);
    printf("=================================================================\n");
    printf("Process PID: %d\n", getpid());

    /* Step 1: Open shared object at runtime */
    printf("[1] Attempting dlopen(\"%s\", RTLD_LAZY)...\n", lib_path);
    void *handle = dlopen(lib_path, RTLD_LAZY);
    if (!handle) {
        fprintf(stderr, "[ERROR] dlopen() failed: %s\n", dlerror());
        fprintf(stderr, "[FALLBACK] Security library unavailable! Bank terminal switching to SAFE OFFLINE MODE.\n");
        return 1;
    }
    printf("[SUCCESS] Library loaded into address space at handle: %p\n", handle);

    /* Clear any existing error */
    dlerror();

    /* Step 2: Resolve symbols dynamically */
    fn_get_version get_version = (fn_get_version)dlsym(handle, "get_encryption_version");
    char *err = dlerror();
    if (err) {
        fprintf(stderr, "[ERROR] dlsym(get_encryption_version) failed: %s\n", err);
        dlclose(handle);
        return 1;
    }

    fn_is_patched is_patched = (fn_is_patched)dlsym(handle, "is_security_patch_active");
    fn_encrypt encrypt = (fn_encrypt)dlsym(handle, "encrypt_payload");
    fn_decrypt decrypt = (fn_decrypt)dlsym(handle, "decrypt_payload");

    printf("[2] Resolved Symbol Addresses:\n");
    printf("    - get_encryption_version at %p\n", (void*)(uintptr_t)get_version);
    printf("    - is_security_patch_active at %p\n", (void*)(uintptr_t)is_patched);
    printf("    - encrypt_payload at %p\n", (void*)(uintptr_t)encrypt);
    printf("    - decrypt_payload at %p\n", (void*)(uintptr_t)decrypt);

    /* Step 3: Execute functions through function pointers */
    printf("\n[3] Library Call Execution:\n");
    printf("    Version: %s\n", get_version());
    printf("    Patch Status: %s\n", (is_patched && is_patched()) ? "SECURE (PATCHED)" : "VULNERABLE (UNPATCHED)");

    const char *payload = "BANK_TX_TRANSFER $500,000 ROUTING_021000021";
    char cipher[128] = {0};
    char plain[128] = {0};
    size_t len = strlen(payload);

    encrypt(payload, cipher, len);
    printf("    Plaintext : %s\n", payload);
    printf("    Ciphertext: ");
    for (size_t i = 0; i < len; i++) printf("%02X ", (unsigned char)cipher[i]);
    printf("\n");

    decrypt(cipher, plain, len);
    printf("    Decrypted : %s\n", plain);

    /* Step 4: Unload library */
    printf("\n[4] Closing library handle with dlclose()...\n");
    dlclose(handle);
    printf("[SUCCESS] Library unloaded from memory space.\n");

    return 0;
}
