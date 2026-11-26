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
