#ifndef LIBENCRYPT_H
#define LIBENCRYPT_H

#include <stddef.h>

const char* get_encryption_version(void);
void encrypt_payload(const char *input, char *output, size_t len);
void decrypt_payload(const char *input, char *output, size_t len);
int is_security_patch_active(void);

#endif /* LIBENCRYPT_H */
