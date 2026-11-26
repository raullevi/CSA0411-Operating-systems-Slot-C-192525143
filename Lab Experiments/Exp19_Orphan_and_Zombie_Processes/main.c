#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    pid_t pid; 
    char cmd[100]; 
  
    /* ----- Zombie process ----- */ 
    pid = fork(); 
    if (pid == 0) { 
        printf("Zombie demo: child %d exits now\n", getpid()); 
        exit(0); 
    } 
    sleep(1); 
    sprintf(cmd, "ps -o pid,ppid,stat,comm -p %d", pid); 
    printf("Process status before wait():\n"); 
    fflush(stdout); 
    system(cmd); 
    wait(NULL); 
    printf("Parent called wait(): zombie %d removed\n\n", pid); 
  
    /* ----- Orphan process ----- */ 
    pid = fork(); 
    if (pid == 0) { 
        if (fork() == 0) { 
            printf("Orphan demo: child %d, parent %d\n", getpid(), getppid()); 
            fflush(stdout); 
            sleep(2); 
            printf("After parent exit: child %d adopted by %d\n", getpid(), getppid()); 
            exit(0); 
        } 
        sleep(1); 
        printf("Parent %d exits, leaving its child as an orphan\n", getpid()); 
        exit(0); 
    } 
    wait(NULL); 
    sleep(3); 
    return 0; 
}
