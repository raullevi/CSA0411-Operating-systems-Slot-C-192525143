#include <stdio.h> 
#include <string.h> 
#include <unistd.h> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <sys/wait.h> 
  
int main() 
{ 
    int shmid = shmget(IPC_PRIVATE, 1024, IPC_CREAT | 0666); 
    if (shmid < 0) { perror("shmget"); return 1; } 
    printf("Shared memory created with id %d\n", shmid); 
    fflush(stdout); 
  
    if (fork() == 0) { 
        char *mem = (char *)shmat(shmid, NULL, 0); 
        strcpy(mem, "Hello from child through shared memory"); 
        printf("Child wrote : %s\n", mem); 
        shmdt(mem); 
        return 0; 
    } 
    wait(NULL); 
    char *mem = (char *)shmat(shmid, NULL, 0); 
    printf("Parent read : %s\n", mem); 
    shmdt(mem); 
    shmctl(shmid, IPC_RMID, NULL); 
    printf("Shared memory removed\n"); 
    return 0; 
}
