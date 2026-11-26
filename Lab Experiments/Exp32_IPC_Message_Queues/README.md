# Experiment 32: IMPLEMENTATION OF MESSAGE QUEUE COMMUNICATION BETWEEN PROCESSES

**Course Outcome:** CO2  
**Course Code:** CSA04 - Operating Systems  
**Student Name:** Rakul K (192525143)  

## AIM
To write a C program to implement communication between processes using a message queue.

## PROCEDURE
1. Define a message structure with a message type and a text field. 
2. Create a message queue using msgget(). 
3. Create a child process using fork(). The child (sender) sends three messages using 
msgsnd(). 
4. The parent (receiver) receives the messages using msgrcv() and displays them. 
5. Remove the message queue using msgctl() with IPC_RMID.

## SOURCE CODE (main.c)
```c
#include <stdio.h> 
#include <string.h> 
#include <unistd.h> 
#include <sys/ipc.h> 
#include <sys/msg.h> 
#include <sys/wait.h> 
  
struct message { 
    long type; 
    char text[100]; 
}; 
  
int main() 
{ 
    struct message m; 
    int i, qid = msgget(IPC_PRIVATE, IPC_CREAT | 0666); 
    char *data[3] = {"Message one", "Message two", "Message three"}; 
  
    printf("Message queue created with id %d\n", qid); 
    fflush(stdout); 
    if (fork() == 0) { 
        for (i = 0; i < 3; i++) { 
            m.type = 1; 
            strcpy(m.text, data[i]); 
            msgsnd(qid, &m, sizeof(m.text), 0); 
            printf("Sender   : sent \"%s\"\n", m.text); 
            fflush(stdout); 
        } 
        return 0; 
    } 
    wait(NULL); 
    for (i = 0; i < 3; i++) { 
        msgrcv(qid, &m, sizeof(m.text), 1, 0); 
        printf("Receiver : got  \"%s\"\n", m.text); 
    } 
    msgctl(qid, IPC_RMID, NULL); 
    printf("Message queue removed\n"); 
    return 0; 
}
```

## EXPECTED & VERIFIED OUTPUT
```
Message queue created with id 2 
Sender   : sent "Message one" 
Sender   : sent "Message two" 
Sender   : sent "Message three" 
Receiver : got  "Message one" 
Receiver : got  "Message two" 
Receiver : got  "Message three" 
Message queue removed
```

## TERMINAL OUTPUT SCREENSHOT

![Exp 32 Terminal Output](exp32_output.png)

## RESULT
Thus communication between processes using a message queue was implemented successfully.
