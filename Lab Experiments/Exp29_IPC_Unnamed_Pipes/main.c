#include <stdio.h> 
#include <string.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    int fd[2]; 
    char msg[] = "Hello child, this is your parent"; 
    char buf[100]; 
  
    if (pipe(fd) == -1) { perror("pipe"); return 1; } 
    if (fork() == 0) { 
        close(fd[1]); 
        int n = read(fd[0], buf, sizeof(buf)); 
        buf[n] = '\0'; 
        printf("Child received  : %s\n", buf); 
        close(fd[0]); 
    } else { 
        close(fd[0]); 
        printf("Parent sending  : %s\n", msg); 
        fflush(stdout); 
        write(fd[1], msg, strlen(msg)); 
        close(fd[1]); 
        wait(NULL); 
        printf("Communication through pipe completed\n"); 
    } 
    return 0; 
}
