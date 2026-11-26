#include <stdio.h> 
#include <unistd.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    char *args[] = {"wc", "-l", "names.txt", NULL}; 
  
    if (fork() == 0) { 
        printf("Child 1 using execl():\n"); 
        fflush(stdout); 
        execl("/bin/echo", "echo", "Hello from execl", NULL); 
        perror("execl"); 
    } 
    wait(NULL); 
  
    if (fork() == 0) { 
        printf("Child 2 using execlp():\n"); 
        fflush(stdout); 
        execlp("ls", "ls", "-1", NULL); 
        perror("execlp"); 
    } 
    wait(NULL); 
  
    if (fork() == 0) { 
        printf("Child 3 using execvp():\n"); 
        fflush(stdout); 
        execvp(args[0], args); 
        perror("execvp"); 
    } 
    wait(NULL); 
    printf("Parent: all children finished\n"); 
    return 0; 
}
