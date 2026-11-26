#include <stdio.h> 
#include <string.h> 
#include <fcntl.h> 
#include <unistd.h> 
  
int main() 
{ 
    char *fname = "sample.txt"; 
    char data[] = "Welcome to Operating Systems Lab\n"; 
    char buf[100]; 
    int fd, n; 
  
    fd = open(fname, O_CREAT | O_WRONLY | O_TRUNC, 0644); 
    if (fd < 0) { perror("open"); return 1; } 
    n = write(fd, data, strlen(data)); 
    printf("File created and %d bytes written\n", n); 
    close(fd); 
  
    fd = open(fname, O_RDONLY); 
    n = read(fd, buf, sizeof(buf) - 1); 
    buf[n] = '\0'; 
    printf("Bytes read : %d\n", n); 
    printf("Contents   : %s", buf); 
    close(fd); 
  
    if (unlink(fname) == 0) 
        printf("File %s deleted\n", fname); 
    if (access(fname, F_OK) != 0) 
        printf("Verified: file no longer exists\n"); 
    return 0; 
}
