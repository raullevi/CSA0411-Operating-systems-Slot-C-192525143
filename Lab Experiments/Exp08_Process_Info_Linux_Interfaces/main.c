#include <stdio.h> 
#include <string.h> 
#include <unistd.h> 
  
int main() 
{ 
    char line[256]; 
    FILE *fp; 
  
    printf("Process ID        : %d\n", getpid()); 
    printf("Parent Process ID : %d\n", getppid()); 
    printf("User ID           : %d\n", getuid()); 
    printf("Group ID          : %d\n", getgid()); 
  
    fp = fopen("/proc/self/status", "r"); 
    if (fp == NULL) { perror("fopen"); return 1; } 
    printf("\nDetails from /proc/self/status:\n"); 
    while (fgets(line, sizeof(line), fp)) { 
        if (strncmp(line, "Name:", 5) == 0 || strncmp(line, "State:", 6) == 0 || 
            strncmp(line, "PPid:", 5) == 0 || strncmp(line, "Threads:", 8) == 0 || 
            strncmp(line, "VmRSS:", 6) == 0) 
            printf("%s", line); 
    } 
    fclose(fp); 
    return 0; 
}
