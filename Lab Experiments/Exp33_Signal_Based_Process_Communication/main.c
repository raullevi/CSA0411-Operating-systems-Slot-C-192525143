#include <stdio.h> 
#include <signal.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
void handler(int sig) 
{ 
    if (sig == SIGUSR1) 
        printf("Child received SIGUSR1: start the task\n"); 
    else if (sig == SIGUSR2) 
        printf("Child received SIGUSR2: stop the task\n"); 
    fflush(stdout); 
} 
  
int main() 
{ 
    int status; 
    signal(SIGUSR1, handler); 
    signal(SIGUSR2, handler); 
  
    pid_t pid = fork(); 
    if (pid == 0) { 
        while (1) 
            pause(); 
    } 
    sleep(1); 
    printf("Parent sending SIGUSR1 to child %d\n", pid); 
    fflush(stdout); 
    kill(pid, SIGUSR1); 
    sleep(1); 
    printf("Parent sending SIGUSR2 to child %d\n", pid); 
    fflush(stdout); 
    kill(pid, SIGUSR2); 
    sleep(1); 
    printf("Parent sending SIGTERM to child %d\n", pid); 
    kill(pid, SIGTERM); 
    wait(&status); 
    if (WIFSIGNALED(status)) 
        printf("Child terminated by signal %d\n", WTERMSIG(status)); 
    return 0; 
}
