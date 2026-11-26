#include <stdio.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    pid_t pid; 
    printf("Before fork: PID = %d\n", getpid()); 
    pid = fork(); 
    if (pid < 0) { 
        printf("Fork failed\n"); 
    } else if (pid == 0) { 
        printf("Child  : PID = %d, Parent PID = %d\n", getpid(), getppid()); 
    } else { 
        wait(NULL); 
        printf("Parent : PID = %d, Child PID = %d\n", getpid(), pid); 
    } 
    return 0; 
}
