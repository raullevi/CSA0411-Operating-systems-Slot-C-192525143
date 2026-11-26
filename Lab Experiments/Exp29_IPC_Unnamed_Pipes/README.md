# Experiment 29: IMPLEMENTATION OF INTER-PROCESS COMMUNICATION USING UNNAMED PIPES

**Course Outcome:** CO2  
**Course Code:** CSA04 - Operating Systems  
**Student Name:** Rakul K (192525143)  

## AIM
To write a C program to implement inter-process communication between a parent and a child 
process using an unnamed pipe.

## PROCEDURE
1. Create a pipe using pipe(fd); fd[0] is the read end and fd[1] is the write end. 
2. Create a child process using fork(). 
3. In the parent, close the read end, write a message into fd[1] and close it. 
4. In the child, close the write end, read the message from fd[0] and display it. 
5. The parent waits for the child to finish.

## SOURCE CODE (main.c)
```c
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
```

## EXPECTED & VERIFIED OUTPUT
```
Parent sending  : Hello child, this is your parent 
Child received  : Hello child, this is your parent 
Communication through pipe completed
```

## TERMINAL OUTPUT SCREENSHOT

![Exp 29 Terminal Output](exp29_output.png)

## RESULT
Thus inter-process communication using an unnamed pipe was implemented successfully.
