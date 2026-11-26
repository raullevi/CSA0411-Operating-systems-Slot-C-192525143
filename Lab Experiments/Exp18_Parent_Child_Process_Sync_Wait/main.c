#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    int status, i; 
    pid_t pid = fork(); 
  
    if (pid == 0) { 
        for (i = 1; i <= 5; i++) 
            printf("Child printing %d\n", i); 
        exit(7); 
    } else { 
        printf("Parent waiting for child %d...\n", pid); 
        fflush(stdout); 
        pid_t done = wait(&status); 
        if (WIFEXITED(status)) 
            printf("Child %d finished with exit status %d\n", done, 
WEXITSTATUS(status)); 
        printf("Parent continues after the child\n"); 
    } 
    return 0; 
}
